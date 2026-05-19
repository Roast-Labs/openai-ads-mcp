"""Ad group tools (read-only)."""

from typing import Any, Optional

from mcp.types import ToolAnnotations

from openai_ads_mcp.client import request
from openai_ads_mcp.coordinator import mcp


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_ad_groups(
    campaign_id: str,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    order: Optional[str] = None,
) -> Any:
    """List ad groups for a campaign."""
    return request(
        "GET",
        "/ad_groups",
        params={
            "campaign_id": campaign_id,
            "limit": limit,
            "after": after,
            "before": before,
            "order": order,
        },
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_ad_group(ad_group_id: str) -> Any:
    """Fetch one ad group by id."""
    return request("GET", f"/ad_groups/{ad_group_id}")
