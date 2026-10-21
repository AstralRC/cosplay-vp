# Unreal Engine scripts

## import_camera_csv.py

Imports the CSV from `colmap_to_ue` (or `cosplay-vp-colmap2ue`) as a keyed CineCamera.

1. Enable the **Python Editor Script Plugin** (Edit → Plugins), restart.
2. Open the Output Log, switch the console to **Python**, and run:
   ```
   py "C:/path/to/import_camera_csv.py" "C:/path/to/camera.csv" 24
   ```
3. Open `/Game/CosplayVP/Seq_TrackedCam`. The camera is `TrackedCam`, keyed once per solved frame, with a camera cut track.
4. Add a cube at a real floor marker and play the shot over the plate. If the cube slides, see `docs/04-camera-tracking.md`.

The CSV columns: `frame, name, x, y, z` (cm), `pitch, yaw, roll` (degrees), `hfov_deg`, `focal_mm_36` (focal length on a 36 mm filmback).

**Status:** written for the UE 5.x Python API and not yet confirmed on every version. If a call fails (Sequencer's Python API changes between releases), open an issue with your engine version and the error.
