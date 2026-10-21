# cosplay-vp

**Open-source tools, AI agent skills and a knowledge base for CG cosplay virtual production.**

Film a real cosplayer on a phone. Cut them out, recover the camera move, put them inside an Unreal Engine world, and finish with anime-style cut-ins and impact frames, for recorded shots or a live event booth.

```
Plan ─► Shoot ─► Prep ─► Matte ─► Track ─► Unreal comp ─► Anime FX ─► Deliver
```

What's in the box:

| Part | What it is |
|---|---|
| [`docs/`](docs/README.md) | Knowledge base: shooting, matting, tracking, Unreal comp, anime FX, live booth architectures (Aximmetry vs Pixel Streaming), rights and consent, open questions |
| [`src/cosplay_vp/`](src/cosplay_vp) | Python library and **MCP server** with 14 tools built on ffmpeg and COLMAP |
| [`skills/`](skills) | 6 **Agent Skills** (SKILL.md) that teach an AI agent the pipeline step by step |
| [`unreal/`](unreal) | Unreal Engine 5 Python script that imports a solved camera as a keyed CineCamera |
| [`tests/`](tests) | Round-trip tests for the COLMAP → Unreal maths and ffmpeg tools on synthetic footage |

## MCP tools

| Tool | Does |
|---|---|
| `probe` | Resolution, fps, rotation, alpha, with warnings for phone quirks |
| `conform` | Constant frame rate, rotation baked in |
| `extract_frames` | Numbered frames for COLMAP or matting |
| `chroma_key` | Green/blue key + despill to ProRes 4444, VP9 alpha or PNG |
| `matte_external` | Runs an AI matting model you installed (RVM, MatAnyone, ...) |
| `composite_preview` | Alpha foreground over a background to check edges |
| `colmap_solve` | COLMAP sparse reconstruction, exported as TXT |
| `colmap_to_ue` | COLMAP cameras → Unreal location (cm), pitch/yaw/roll, FOV, focal length |
| `on_twos` | Anime "on twos" timing |
| `impact_frames` | Invert or white flash frames on hits |
| `side_by_side` | Raw vs final demo |
| `vertical` | 9:16 crop for TikTok, Reels and Shorts |
| `latency_budget` | Plan a live booth's latency against a target |
| `knowledge` | Read any page of the knowledge base |

## Quick start

Requirements: Python 3.10+, [ffmpeg](https://ffmpeg.org/download.html). Optional: [COLMAP](https://colmap.github.io/install.html), Unreal Engine 5, Blender, OBS.

```bash
git clone https://github.com/<your-org>/cosplay-vp.git
cd cosplay-vp
pip install -e ".[dev]"
pytest            # 14 tests, including a live MCP stdio session
```

### Connect the MCP server

**Claude Code**

```bash
claude mcp add cosplay-vp -- cosplay-vp-mcp
```

**Claude Desktop** (`claude_desktop_config.json`), or any MCP client:

```json
{
  "mcpServers": {
    "cosplay-vp": { "command": "cosplay-vp-mcp" }
  }
}
```

If the command isn't on your PATH, use `"command": "python", "args": ["-m", "cosplay_vp.server"]`.

### Install the skills

- **Claude Code:** copy the folders in `skills/` to `~/.claude/skills/` (all projects) or `.claude/skills/` (one project).
- **Claude apps:** zip a skill folder and upload it under Settings → Capabilities → Skills.

Then ask, for example:

> Plan a 15-second ultimate-move cut-in for an original character, then prep `take3.mp4`, key it, and track the camera into Unreal.

### Without an AI agent

```bash
cosplay-vp-colmap2ue colmap_ws/sparse_txt camera.csv --scale 100
```

and in Unreal's Python console:

```
py "path/to/unreal/import_camera_csv.py" "path/to/camera.csv" 24
```

## Status

| Area | Status |
|---|---|
| ffmpeg tools, COLMAP → UE conversion | Working, tested in CI |
| `colmap_solve` | Wraps the COLMAP CLI; needs COLMAP installed |
| Unreal import script | Written for UE 5.x, not yet tested across versions; reports welcome |
| Live booth architectures B and C (cloud) | Hypotheses, see [doc 07](docs/07-live-booth-architectures.md) and [doc 09](docs/09-open-questions-and-benchmarks.md) |

## Roadmap

1. **Local booth prototype:** Unreal + OBS key, measured latency.
2. **Cloud experiment:** Pixel Streaming with a camera uplink, latency against the local build.
3. **Matting benchmark:** hair and lace edges, speed per model.
4. **Unreal MCP bridge:** place media plates and queue Movie Render Queue jobs from an agent.
5. **Rotation-only (nodal) solve** for tripod pans.

## Ground rules

- Only film people who agreed, with guardian consent for anyone under 18.
- Paid work uses characters the client owns or licensed, or original characters.
- No ripped game assets, logos or music in this repo.
- Label ads, and label AI-generated content where platforms require it.

Details: [docs/08-rights-consent-disclosure.md](docs/08-rights-consent-disclosure.md).

## Contributing

Benchmarks with methods, fixes for new Unreal versions, matting comparisons and translations are all welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Code: [MIT](LICENSE). Docs and skills: [CC BY 4.0](LICENSE-docs). External tools keep their own licences ([doc 10](docs/10-tools-and-licences.md)).

Started by Idea (Phakpaphon Jaiwanglok) of [AstralRC](https://www.youtube.com/@Astral_RC) / CELESTI.
