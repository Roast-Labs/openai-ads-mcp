"""Ad account tools (GET /ad_account)."""

from typing import Any

from mcp.types import ToolAnnotations

from openai_ads_mcp.client import request
from openai_ads_mcp.coordinator import mcp


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_ad_account() -> Any:
    """Return metadata for the current ad account (id, name, urls, timezone, currency).

    See https://developers.openai.com/ads/api-reference/ad-account
    """
    return request("GET", "/ad_account")
