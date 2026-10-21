# 01 Pipeline overview

**Status:** Established. This is the pipeline the project's tools are built around.

The idea: a real cosplayer performs on a phone or camera. We cut them out, recover how the camera moved, and place them inside an Unreal Engine set that moves with the same camera. Then we add the visual language of anime and games: cut-ins, impact frames, held frames.

```
Plan ─► Shoot ─► Prep ─► Matte ─► Track ─► Unreal comp ─► Anime FX ─► Deliver
 │        │        │        │        │          │             │           │
shot    plate   conform  key or   COLMAP    media plate   on twos,    9:16,
sheet   + clean  + frames  AI matte  solve →   + CG set,    impact      side-by-
consent  plate                     UE camera  light match  frames,     side demo
                                              + shadows    cut-ins
```

## The stages

| Stage | Goal | Tools in this repo | Doc |
|---|---|---|---|
| Plan | One clear character moment, a shot sheet, consent and rights in writing | `cosplay-vp-shot-planner` skill | 02, 08 |
| Shoot | A plate that keys and tracks: locked exposure, fixed frame rate, markers, clean plate | checklist in skill | 02 |
| Prep | Constant frame rate, rotation baked in, numbered frames | `probe`, `conform`, `extract_frames` | 02 |
| Matte | Performer with a clean alpha | `chroma_key`, `matte_external`, `composite_preview` | 03 |
| Track | A camera path that matches the plate | `colmap_solve`, `colmap_to_ue`, `unreal/import_camera_csv.py` | 04 |
| Comp | Performer sits in the world: light, colour, contact shadows, depth | Unreal Engine (Composure / media plate) | 05 |
| FX | The anime read: timing, impact, cut-ins, titles | `on_twos`, `impact_frames`, After Effects or Unreal | 06 |
| Deliver | Vertical cuts and a before/after demo | `vertical`, `side_by_side` | 06 |

## Two modes

- **Recorded shots** (Reels, MVs, ads): quality first, every stage above, minutes to hours per shot.
- **Live booth** (events): speed first, fixed camera, real-time key, no tracking at first. See 07.

## Working with an AI agent

The MCP server exposes each step as a tool and the skills tell the agent the order and the checks. A typical prompt:

> "Probe `clip.mp4`, conform it to 24 fps, extract frames at 12 fps, solve the camera with COLMAP, and give me a UE camera CSV at 1 unit = 1 m."

The agent should stop and show you results at three checkpoints: the matte edge, the test-cube track, and the first comp frame. Those are where most shots fail.
