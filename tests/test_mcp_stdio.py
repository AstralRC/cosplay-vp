"""Start the MCP server over stdio and call tools like a real client would."""

import asyncio
import sys

import pytest

mcp = pytest.importorskip("mcp")

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:  # pragma: no cover
    pytest.skip("MCP client API not available", allow_module_level=True)


async def _session_calls():
    params = StdioServerParameters(command=sys.executable, args=["-m", "cosplay_vp.server"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = {t.name for t in tools.tools}
            result = await session.call_tool("latency_budget", {"stages_ms": {"camera": 40, "render": 20}, "target_ms": 100})
            topics = await session.call_tool("knowledge", {})
            return names, result, topics


def test_server_over_stdio():
    names, result, topics = asyncio.run(_session_calls())
    assert {"probe", "chroma_key", "colmap_to_ue", "knowledge"} <= names
    text = "".join(getattr(c, "text", "") for c in result.content)
    assert "60" in text
    assert "07-live-booth-architectures" in "".join(getattr(c, "text", "") for c in topics.content)
