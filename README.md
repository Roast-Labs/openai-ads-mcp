# OpenAI ChatGPT Ads MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that
exposes the [ChatGPT Ads API](https://developers.openai.com/ads/api-reference/authentication)
(`https://api.ads.openai.com/v1`) as tools an LLM host can call. Runs as a plain
Python process — no cloud platform required.

## What it exposes

Tools map to the Advertiser API documented under
[Ads → API Reference](https://developers.openai.com/ads/api-reference/authentication):

| Area        | Tools |
| ----------- | ----- |
| Ad account  | `get_ad_account` |
| Campaigns   | `list_campaigns`, `get_campaign` |
| Ad groups   | `list_ad_groups`, `get_ad_group` |
| Ads         | `list_ads`, `get_ad` |
| Insights    | `get_ad_account_insights`, `get_campaign_insights`, `get_ad_group_insights`, `get_ad_insights` |

Only **read/list/report** tools are registered (`GET`-equivalent Ads calls).
Mutating actions (create/update/activate/pause/archive/upload) are omitted **for now**.
All exposed tools set read-only hints (`readOnlyHint`) for MCP clients.

## Architecture

```
python -m openai_ads_mcp          stdio (Cursor, Claude Desktop, etc.)
python -m openai_ads_mcp --transport http   streamable HTTP (remote clients)
  └─ openai_ads_mcp/server.py     registers every tool
       ├─ coordinator.py          FastMCP singleton
       ├─ client.py               httpx wrapper + bearer auth
       └─ tools/                   resource modules
```

- **Single registration point.** `openai_ads_mcp/server.py` imports all tool modules.
- **Two transports.** Stdio for local IDE hosts; HTTP for remote MCP clients (e.g. via ngrok).

## Authentication

- **This server → Ads API.** Set `OPENAI_ADS_API_KEY` (header
  `Authorization: Bearer …` per the
  [authentication docs](https://developers.openai.com/ads/api-reference/authentication)).
- **Caller → this server.** Not enforced by default. Put auth (API gateway, reverse proxy,
  VPN, etc.) in front of HTTP mode if you expose it publicly.

**Secrets:** keep Ads keys out of git — copy `.env.example` to `.env` and add your key there.
Never commit real keys.

## Quick start

### Prerequisites

- **Python 3.11+**
- An OpenAI Ads API key

### Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
pip install -e .
```

Copy the example env file and add your key:

```powershell
copy .env.example .env
# Edit .env and set OPENAI_ADS_API_KEY
```

### Run (stdio — for Cursor and other IDE MCP hosts)

The process **blocks with little or no visible output**: MCP uses **stdin/stdout**
for JSON-RPC. You should see a one-line notice on **stderr**; do not run the
server interactively in a normal terminal expecting a prompt.

```powershell
python -m openai_ads_mcp
```

Equivalent commands:

```powershell
openai-ads-mcp
python -m openai_ads_mcp.server
```

**Cursor MCP config** — use your venv's `python.exe` as `command`, project root as `cwd`:

```json
{
  "mcpServers": {
    "openai-ads": {
      "command": "C:\\path\\to\\chatgptads-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "openai_ads_mcp"],
      "cwd": "C:\\path\\to\\chatgptads-mcp"
    }
  }
}
```

Or set `OPENAI_ADS_API_KEY` in the `env` block instead of using `.env`.

### Run (HTTP — for remote MCP clients)

```powershell
python -m openai_ads_mcp --transport http --host 127.0.0.1 --port 8000
```

Point remote MCP clients at `http://127.0.0.1:8000/mcp`. To expose publicly, tunnel
with ngrok or similar and add auth at the gateway layer.

## Environment variables

| Variable | Required | Description |
| -------- | -------- | ----------- |
| `OPENAI_ADS_API_KEY` | Yes | Ads API key |

## Project layout

```
requirements.txt
pyproject.toml
.env.example
openai_ads_mcp/
  __main__.py
  server.py
  coordinator.py
  client.py
  tools/
    ad_account.py
    campaigns.py
    ad_groups.py
    ads.py
    insights.py
```

See also `capabilities.md` for a full tool reference.
