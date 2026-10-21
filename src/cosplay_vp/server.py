"""MCP server: CG cosplay virtual production tools for AI agents.

Run:  cosplay-vp-mcp            (stdio, for Claude Desktop / Claude Code)
      python -m cosplay_vp.server

Works with the MCP Python SDK v1 (FastMCP) and v2 (MCPServer).
"""

from __future__ import annotations

from pathlib import Path

try:  # MCP Python SDK 2.x
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # MCP Python SDK 1.x
    from mcp.server.fastmcp import FastMCP as _Server

from . import colmap_ue, media

INSTRUCTIONS = """Tools for CG cosplay virtual production: real cosplayers filmed on a phone or
camera, cut out (chroma key or AI matting), camera-tracked with COLMAP, and finished
in Unreal Engine with anime-style effects. Typical order: probe -> conform ->
extract_frames -> colmap_solve -> colmap_to_ue -> chroma_key / matte_external ->
composite_preview -> on_twos / impact_frames -> side_by_side / vertical.
Read the `knowledge` tool for the method behind each step. Only work with footage
the performer agreed to, and only with characters the client owns or licensed."""

mcp = _Server("cosplay-vp", instructions=INSTRUCTIONS)

DOCS_DIR = Path(__file__).resolve().parents[2] / "docs"


def _safe(fn, *args, **kwargs) -> dict:
    try:
        return {"ok": True, **fn(*args, **kwargs)}
    except media.ToolMissing as e:
        return {"ok": False, "missing_tool": str(e)}
    except Exception as e:  # report, don't crash the server
        return {"ok": False, "error": str(e)}


@mcp.tool()
def probe(path: str) -> dict:
    """Inspect a clip: resolution, fps, duration, codec, rotation, alpha, plus warnings (variable frame rate, rotation flags)."""
    return _safe(media.probe, path)


@mcp.tool()
def conform(input: str, output: str, fps: float = 24.0) -> dict:
    """Re-encode phone footage to a constant frame rate with rotation baked in. Do this before tracking or matting."""
    return _safe(media.conform, input, output, fps)


@mcp.tool()
def extract_frames(input: str, out_dir: str, fps: float | None = None, start: float | None = None,
                   duration: float | None = None, ext: str = "jpg") -> dict:
    """Export numbered frames (00001.jpg ...) for COLMAP or matting. Use fps to thin long clips."""
    return _safe(media.extract_frames, input, out_dir, fps, start, duration, ext)


@mcp.tool()
def chroma_key(input: str, output: str, color: str = "0x00FF00", similarity: float = 0.12,
               blend: float = 0.06, despill: bool = True) -> dict:
    """Green/blue screen key to a clip with alpha (.mov ProRes 4444, .webm VP9, or %05d.png). A fast first pass."""
    return _safe(media.chroma_key, input, output, color, similarity, blend, despill)


@mcp.tool()
def matte_external(input: str, output: str, command_template: str) -> dict:
    """Run an AI matting tool the user installed (e.g. RVM, MatAnyone) using {input}/{output} placeholders. Check that tool's licence first."""
    return _safe(media.matte_external, input, output, command_template)


@mcp.tool()
def composite_preview(foreground: str, background: str, output: str, height: int = 1080) -> dict:
    """Preview an alpha foreground over a background still or render. For checking edges, not the final comp."""
    return _safe(media.composite_preview, foreground, background, output, height)


@mcp.tool()
def colmap_solve(image_dir: str, workspace: str, quality: str = "medium", single_camera: bool = True) -> dict:
    """Solve the camera from a frame folder with COLMAP (must be installed) and export the model as TXT."""
    return _safe(media.colmap_solve, image_dir, workspace, quality, single_camera)


@mcp.tool()
def colmap_to_ue(sparse_txt_dir: str, output: str, scale: float = 100.0) -> dict:
    """Convert COLMAP cameras.txt + images.txt into Unreal camera keys (.csv or .json): location in cm, pitch/yaw/roll, FOV.
    scale = UE centimetres per COLMAP unit. Import with unreal/import_camera_csv.py."""
    return _safe(colmap_ue.convert_folder, sparse_txt_dir, output, scale)


@mcp.tool()
def on_twos(input: str, output: str, hold: int = 2, fps: float | None = None) -> dict:
    """Give motion the anime 'on twos' feel by holding each frame `hold` times at the same frame rate."""
    return _safe(media.on_twos, input, output, hold, fps)


@mcp.tool()
def impact_frames(input: str, output: str, frames: list[int], length: int = 2, mode: str = "invert") -> dict:
    """Add anime impact flashes at frame numbers. mode: 'invert' or 'white'."""
    return _safe(media.impact_frames, input, output, frames, length, mode)


@mcp.tool()
def side_by_side(before: str, after: str, output: str, height: int = 1080) -> dict:
    """Raw plate next to the finished shot, for showreels and pitch demos."""
    return _safe(media.side_by_side, before, after, output, height)


@mcp.tool()
def vertical(input: str, output: str, width: int = 1080, height: int = 1920) -> dict:
    """Fill-crop a render to 9:16 for TikTok, Reels and Shorts."""
    return _safe(media.vertical, input, output, width, height)


@mcp.tool()
def latency_budget(stages_ms: dict[str, float], target_ms: float = 100.0) -> dict:
    """Sum estimated latency per stage of a live booth (camera, key, render, stream, display) against a target."""
    return _safe(media.latency_budget, stages_ms, target_ms)


@mcp.tool()
def knowledge(topic: str | None = None) -> dict:
    """Read the project's knowledge base. Call with no topic to list topics."""
    files = sorted(DOCS_DIR.rglob("*.md")) if DOCS_DIR.exists() else []
    if not files:
        return {"ok": False, "error": f"Docs folder not found at {DOCS_DIR}. Install from a git clone (pip install -e .)."}
    index = {f.stem: f for f in files}
    if not topic:
        return {"ok": True, "topics": list(index)}
    match = index.get(topic) or next((f for k, f in index.items() if topic.lower() in k.lower()), None)
    if not match:
        return {"ok": False, "error": f"No topic '{topic}'", "topics": list(index)}
    return {"ok": True, "topic": match.stem, "markdown": match.read_text()}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
