# How we built this

**Status:** A transparent record of how the first version was made, so others can check the work and repeat the method.

## Who and how

The project was started by Idea (Phakpaphon Jaiwanglok) of AstralRC, from techniques developed on his own Unreal Engine virtual production projects. The first version of the code, docs and skills was written with Claude (Anthropic) as a coding agent, directed and reviewed by Idea. "Made with Claude" means the tool was used; it doesn't mean Anthropic endorses the project.

## The method: direct → check → fix

The same loop the [prompt library](prompts.md) teaches:

1. **Direct.** A plain-language request: build an open-source toolkit, MCP server and knowledge base for CG cosplay virtual production, starting from our notes on Aximmetry vs Pixel Streaming.
2. **Check.** Every claim that could be tested was tested before release (below). Anything that couldn't be tested is labelled as untested or as a hypothesis in the docs.
3. **Fix.** Failures found during the build were fixed and are listed here.

## What was tested, and how

| Part | Test | Result |
|---|---|---|
| COLMAP → Unreal conversion | Round trip: known Unreal cameras → synthetic COLMAP data → converter → compare | Matches to 1e-6 on 5 cameras, including roll and steep pitch |
| Handedness of the axis mapping | Determinant of the mapping matrix | −1, as required (right-handed → left-handed) |
| ffmpeg tools | A generated green-screen clip run through key, preview, on twos, impact frames, side by side, vertical | All outputs have the expected size, frame rate and alpha |
| MCP server | Started over stdio and called by a real MCP client | Tools listed and answered |
| Unreal import script | Compiles; written against the UE 5.x Python API | **Not yet run inside Unreal.** Reports welcome |
| COLMAP solve wrapper | Missing-tool handling tested; the solve itself needs COLMAP installed | Needs a real-footage test |
| Cloud booth architectures | None yet | Hypotheses, see [open questions](09-open-questions-and-benchmarks.md) |

## Bugs found during the build

- **Composite frame rate.** A still background looped at ffmpeg's default 25 fps changed a 24 fps comp to 25 fps. Fixed by looping the still at the foreground's frame rate. A test now checks it.
- **MCP SDK v2 rename.** `FastMCP` became `MCPServer` in the MCP Python SDK v2. The server now imports either.

## Decisions

- **No AI models bundled.** Matting models carry their own licences (RVM: GPL-3.0; MatAnyone: NTU S-Lab License 1.0), so the server runs whichever one you install.
- **No game assets.** Examples use original characters only; see [rights and consent](08-rights-consent-disclosure.md).
- **External tools are called, not linked.** ffmpeg and COLMAP run as separate programs with argument lists, never shell strings.

## Run the checks yourself

```bash
pip install -e ".[dev]"
pytest -v
```
