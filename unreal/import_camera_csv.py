"""Import a cosplay-vp camera CSV into Unreal Engine 5 as a keyed CineCamera.

Run inside the Unreal Editor (Python Editor Script Plugin enabled):
    Tools > Execute Python Script...  or  in the Output Log Python console:
    py "C:/path/to/import_camera_csv.py" "C:/path/to/camera.csv" 24

What it does:
  1. Spawns a CineCameraActor named TrackedCam.
  2. Sets its focal length from the CSV on a 36 x 20.25 mm filmback.
  3. Creates /Game/CosplayVP/Seq_TrackedCam with the camera bound and one
     transform key per solved frame (location cm, rotation degrees).

Check after import: add a cube where the floor should be. If it slides
against the plate, the solve, scale or gravity alignment is wrong.

Status: written against the UE 5.x Python API; tested only on the CSV
side in CI. Please report your engine version in an issue if it breaks.
"""

import csv
import sys

import unreal

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else ""
FPS = int(sys.argv[2]) if len(sys.argv) > 2 else 24
SEQ_DIR = "/Game/CosplayVP"
SEQ_NAME = "Seq_TrackedCam"


def load_rows(path):
    with open(path, newline="") as f:
        return [{k: (v if k == "name" else float(v)) for k, v in row.items()} for row in csv.DictReader(f)]


def main():
    if not CSV_PATH:
        unreal.log_error("Usage: py import_camera_csv.py <camera.csv> [fps]")
        return
    rows = load_rows(CSV_PATH)
    if not rows:
        unreal.log_error("CSV has no rows")
        return

    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    cam = actors.spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector(0, 0, 0))
    cam.set_actor_label("TrackedCam")
    comp = cam.get_cine_camera_component()
    filmback = comp.get_editor_property("filmback")
    filmback.set_editor_property("sensor_width", 36.0)
    filmback.set_editor_property("sensor_height", 20.25)
    comp.set_editor_property("filmback", filmback)
    comp.set_editor_property("current_focal_length", rows[0]["focal_mm_36"])

    tools = unreal.AssetToolsHelpers.get_asset_tools()
    seq = tools.create_asset(SEQ_NAME, SEQ_DIR, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    seq.set_display_rate(unreal.FrameRate(FPS, 1))
    first, last = int(rows[0]["frame"]), int(rows[-1]["frame"])
    seq.set_playback_start(first)
    seq.set_playback_end(last + 1)

    binding = seq.add_possessable(cam)
    track = binding.add_track(unreal.MovieScene3DTransformTrack)
    section = track.add_section()
    section.set_range(first, last + 1)

    # Transform channel order: Location X Y Z, Rotation X(roll) Y(pitch) Z(yaw), Scale X Y Z
    if hasattr(section, "get_all_channels"):
        ch = section.get_all_channels()
    else:  # newer API
        ch = section.get_channels_by_type(unreal.MovieSceneScriptingDoubleChannel)
    for r in rows:
        f = unreal.FrameNumber(int(r["frame"]))
        ch[0].add_key(f, r["x"])
        ch[1].add_key(f, r["y"])
        ch[2].add_key(f, r["z"])
        ch[3].add_key(f, r["roll"])
        ch[4].add_key(f, r["pitch"])
        ch[5].add_key(f, r["yaw"])

    # Camera cut so the sequence looks through the tracked camera.
    # The binding-ID API differs between UE 5 releases, so failure here is not fatal.
    try:
        add = seq.add_track if hasattr(seq, "add_track") else seq.add_master_track
        cuts = add(unreal.MovieSceneCameraCutTrack)
        cut = cuts.add_section()
        cut.set_range(first, last + 1)
        if hasattr(seq, "get_binding_id"):
            cut.set_camera_binding_id(seq.get_binding_id(binding))
        else:
            cut.set_camera_binding_id(seq.make_binding_id(binding, unreal.MovieSceneObjectBindingSpace.LOCAL))
    except Exception as e:  # noqa: BLE001
        unreal.log_warning(f"cosplay-vp: camera cut not added ({e}); pilot TrackedCam manually")

    unreal.EditorAssetLibrary.save_loaded_asset(seq)
    unreal.log(f"cosplay-vp: keyed {len(rows)} frames ({first}-{last}) at {FPS} fps into {SEQ_DIR}/{SEQ_NAME}")


main()
