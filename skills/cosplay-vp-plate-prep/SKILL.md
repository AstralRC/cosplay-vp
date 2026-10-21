---
name: cosplay-vp-plate-prep
description: Prepare cosplay footage after filming - probe, conform phone video to a fixed frame rate, extract frames, and cut the performer out with chroma key or an AI matting tool. Use when someone has raw cosplay clips to key, matte, or get ready for tracking and Unreal.
---

# Cosplay VP plate prep

Uses the `cosplay-vp` MCP tools when connected; otherwise give the equivalent ffmpeg commands from `src/cosplay_vp/media.py`.

## Steps

1. **Probe every clip** with `probe`. Report resolution, fps, duration, rotation and warnings. Variable frame rate or a rotation flag means conform first.
2. **Conform** with `conform(input, output, fps=24)` (or the project's rate). Work from the conformed file from now on.
3. **Frames** if the clip will be tracked: `extract_frames(input, out_dir, fps=12)` for the solve. Keep full-rate frames for matting if the matting tool wants images.
4. **Cut out the performer:**
   - Screen shot: `chroma_key(input, "keyed.mov")`. Start at similarity 0.12, blend 0.06. Raise similarity until the screen is gone; raise blend if the edge is hard.
   - No screen, or hair and motion blur failing: `matte_external` with the user's installed model. Ask which one they have and its command. Remind them of the model's licence (RVM is GPL-3.0; MatAnyone is NTU S-Lab License 1.0) before commercial use.
   - Hybrid: key for the body, AI matte for hair, combined in the compositor (`docs/03-matting-and-keying.md`).
5. **Check the matte.** Run `composite_preview` over a mid-grey still and a bright still. Show both to the user and ask them to look at hair, fingers and prop edges at full size. Don't move on until they approve.

## Reporting

End with a short table: clip, fps after conform, matte method, output path, open issues (fringe, flicker, prop edges). Next skill: `cosplay-vp-camera-track` for moving shots, `cosplay-vp-unreal-comp` for locked-off ones.

## Don't

- Don't key the original phone file directly when it has variable frame rate.
- Don't bundle or download matting models into the user's project without telling them the licence.
- Don't process footage of people who haven't agreed to it.
