# 04 Camera tracking

**Status:** Established. The COLMAP → Unreal converter in this repo is unit-tested; the in-editor import script is written for UE 5.x and needs reports from more engine versions.

Tracking recovers how the real camera moved, so the virtual camera can move the same way. Without it the performer slides against the world.

## Do you need it?

| Shot | Tracking |
|---|---|
| Locked-off tripod | No. Match the lens and angle once |
| Tripod pan or tilt only | Rotation-only (nodal) solve, not COLMAP |
| Handheld, dolly, push-in | Yes, a full 3D solve |

## Route A: COLMAP (automatic, open source)

1. `conform` the clip to a fixed frame rate.
2. `extract_frames` at 8–12 fps for the solve (more frames = slower, rarely better).
3. Mask out the performer if you can: moving people confuse structure-from-motion. Markers on the screen and floor give it static features.
4. `colmap_solve(image_dir, workspace)` runs `automatic_reconstructor` with `--data_type video --single_camera 1` and exports TXT.
5. `colmap_to_ue(sparse_txt_dir, "camera.csv", scale=100)` writes one row per solved frame: location in cm, pitch/yaw/roll, horizontal FOV and focal length on a 36 mm filmback.
6. In Unreal, run `unreal/import_camera_csv.py camera.csv 24` to get a keyed CineCamera and a Level Sequence.

**Coordinates.** COLMAP uses x right, y down, z forward (right-handed). Unreal uses X forward, Y right, Z up (left-handed, cm). The converter maps `(X, Y, Z) = (z, x, -y)`, which also flips handedness. The rotator maths follows Unreal's `FRotationMatrix`, and the tests round-trip known cameras.

**Scale and gravity.** COLMAP doesn't know which way is down or how big the scene is.
- Gravity: run `colmap model_orientation_aligner` on the model, or rotate the solve in Blender before export.
- Scale: measure the distance between two markers in the solve and set `scale` so it matches the real distance you wrote on the shot sheet.

**Frames missing from the solve.** The converter reports gaps. If frames were extracted at a lower rate than the plate, interpolate keys in Sequencer, or extract every frame for the final solve.

## Route B: Blender camera tracker

Blender's Movie Clip Editor tracks 2D features by hand or automatically and solves the camera. Good for difficult shots where you want control. Export the camera to Unreal as FBX, or to COLMAP-style data with community add-ons.

## Prove the track (always)

1. Put a cube on the virtual floor, where a real floor marker is.
2. Play the shot over the plate.
3. If the cube stays glued to the marker, the track is good. If it slides: check frame rate, the lens, scale, and missing frames, in that order.

## When the solve fails

| Symptom | Likely cause |
|---|---|
| No model, or many small models | Too little texture or parallax; add markers, move the camera more |
| Model drifts over time | Rolling shutter or zoom; shorten the shot or re-shoot |
| Right path, wrong size | Scale not set |
| Right path, tilted world | Gravity not aligned |
| Wobbly at the start or end | Fewer features at the edges; trim or hand-fix keys |
