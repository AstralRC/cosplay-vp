---
name: cosplay-vp-camera-track
description: Solve the real camera move from cosplay footage with COLMAP and bring it into Unreal Engine as a keyed CineCamera, then prove it with a test cube. Use when a handheld or moving shot needs the virtual set to move with the camera.
---

# Cosplay VP camera track

Background and coordinate maths: `docs/04-camera-tracking.md`.

## Decide first

- Locked-off tripod: no tracking. Match the lens and height in Unreal and skip this skill.
- Pan/tilt only on a tripod: needs a rotation-only solve, not COLMAP. Say so.
- Handheld, dolly or push-in: continue.

## Steps

1. Frames: `extract_frames(conformed_clip, "frames", fps=12)`. Mask or crop out the performer if possible; static markers help COLMAP.
2. Solve: `colmap_solve("frames", "colmap_ws")`. If it returns `missing_tool`, give the COLMAP install link and stop. If several models come back, the solve broke apart: suggest more frames, more markers or a shorter shot.
3. Fix gravity: suggest `colmap model_orientation_aligner` on the model, or aligning in Blender.
4. Set scale: ask for the measured distance on the shot sheet. Explain that `scale` = UE cm per COLMAP unit, and work it out from the distance between the two markers in the solve.
5. Convert: `colmap_to_ue("colmap_ws/sparse_txt", "camera.csv", scale=...)`. Report solved frames and gaps.
6. Import into Unreal: `py unreal/import_camera_csv.py camera.csv 24` in the editor's Python console. It creates `TrackedCam` and `/Game/CosplayVP/Seq_TrackedCam`.
7. **Prove it:** a cube on the virtual floor at a real floor marker, played over the plate. Ask the user to confirm it stays put. If it slides, check in order: frame rate, lens, scale, gravity, missing frames.

## Report

Solved frames / total, gaps, scale used, FOV, and the test-cube result. Next: `cosplay-vp-unreal-comp`.
