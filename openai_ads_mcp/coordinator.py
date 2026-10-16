"""Singleton FastMCP instance for the OpenAI Ads MCP server."""

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

mcp = FastMCP(
    "OpenAI Ads Server",
    # Cursor/streamable-HTTP clients often advertise JSON Accept without SSE;
    # SDK accepts POST when json_response=True; SSE-only validation stays on GET.
    json_response=True,
    stateless_http=True,
    # Railway forwards requests with its public domain as Host header.
    # Bearer auth (MCP_AUTH_TOKEN) remains the access control.
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["openai-ads-mcp-production-4624.up.railway.app"],
    ),
)
