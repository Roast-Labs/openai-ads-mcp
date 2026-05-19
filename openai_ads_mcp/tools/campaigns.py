"""Campaign tools (read-only)."""

from typing import Any, Optional

from mcp.types import ToolAnnotations

from openai_ads_mcp.client import request
from openai_ads_mcp.coordinator import mcp


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_campaigns(
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    order: Optional[str] = None,
) -> Any:
    """List campaigns in the current ad account (pagination + sort).

    See https://developers.openai.com/ads/api-reference/campaigns
    """
    return request(
        "GET",
        "/campaigns",
        params={
            "limit": limit,
            "after": after,
            "before": before,
            "order": order,
        },
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_campaign(campaign_id: str) -> Any:
    """Fetch one campaign by id."""
    return request("GET", f"/campaigns/{campaign_id}")
