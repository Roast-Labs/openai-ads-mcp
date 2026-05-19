"""Entry point for the OpenAI Ads MCP server."""

from __future__ import annotations

import argparse
import sys

from openai_ads_mcp.coordinator import mcp

from openai_ads_mcp.tools import (  # noqa: F401
    ad_account,
    ad_groups,
    ads,
    campaigns,
    insights,
)


def run_stdio() -> None:
    """Run the MCP server over stdin/stdout (default for IDE hosts like Cursor)."""
    print(
        "OpenAI Ads MCP: listening on stdio for an MCP client (e.g. Cursor). "
        "No stdout until the client connects; exiting with Ctrl+C is normal if "
        "you started this by hand.",
        file=sys.stderr,
        flush=True,
    )
    mcp.run(transport="stdio")


def run_http(host: str, port: int) -> None:
    """Run the MCP server over streamable HTTP (for remote MCP clients)."""
    import uvicorn

    print(
        f"OpenAI Ads MCP: listening on http://{host}:{port}/mcp",
        file=sys.stderr,
        flush=True,
    )
    uvicorn.run(mcp.streamable_http_app(), host=host, port=port, log_level="warning")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="OpenAI ChatGPT Ads MCP server",
    )
    parser.add_argument(
        "--transport",
        choices=("stdio", "http"),
        default="stdio",
        help="stdio for local IDE hosts (default); http for remote clients",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP bind address (http transport only)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP bind port (http transport only)",
    )
    args = parser.parse_args(argv)

    if args.transport == "http":
        run_http(args.host, args.port)
    else:
        run_stdio()


if __name__ == "__main__":
    main()
