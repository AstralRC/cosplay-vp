# 10 Tools and licences

**Status:** Reference. Licences change; check each project's own licence file before you ship commercial work.

| Tool | Role in the pipeline | Licence or terms | Used by this repo |
|---|---|---|---|
| [ffmpeg](https://ffmpeg.org/) | Probe, conform, key, preview, timing FX, delivery | LGPL/GPL depending on build | Required |
| [COLMAP](https://colmap.github.io/) | Camera solve (structure from motion) | BSD | Optional (`colmap_solve`) |
| [Unreal Engine 5](https://www.unrealengine.com/) | Real-time rendering, compositing, Sequencer, Movie Render Queue | Epic Games EULA | Target engine |
| [Blender](https://www.blender.org/) | Modelling, camera tracking, solve clean-up | GPL | Optional |
| [OBS Studio](https://obsproject.com/) | Live keying, scene layering, recording | GPL-2.0 | Booth v0 |
| [Pixel Streaming Infrastructure](https://github.com/EpicGamesExt/PixelStreamingInfrastructure) | Stream Unreal output to a browser | See repository | Architecture B |
| [Aximmetry](https://aximmetry.com/) | Live virtual production, tracking, compositing | Commercial (editions vary) | Architecture A/C |
| NDI tools | Video over a local network between apps | Proprietary, free tools available | Booth v0 option |
| [TouchDesigner](https://derivative.ca/) | Interactive installations, sensors | Commercial, with a non-commercial edition | Optional |
| Robust Video Matting | AI person matting | GPL-3.0 | Via `matte_external`, not bundled |
| MatAnyone | AI video matting, strong on hair | NTU S-Lab License 1.0 | Via `matte_external`, not bundled |
| Adobe After Effects | Post VFX, cut-in graphics | Commercial | Optional |
| DaVinci Resolve | Edit, colour, keying | Free and paid editions | Optional |

## This repository

- Code: MIT (see `LICENSE`).
- Documentation in `docs/` and `skills/`: CC BY 4.0 (see `LICENSE-docs`).
- The MCP server calls external tools as separate programs; it doesn't include or link their code.
