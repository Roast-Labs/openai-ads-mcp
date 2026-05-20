"""Singleton FastMCP instance for the OpenAI Ads MCP server."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "OpenAI Ads Server",
    # Cursor/streamable-HTTP clients often advertise JSON Accept without SSE;
    # SDK accepts POST when json_response=True; SSE-only validation stays on GET.
    json_response=True,
    stateless_http=True,
)
