"""Ad creative / placement tools (read-only)."""

from typing import Any, Optional

from mcp.types import ToolAnnotations

from openai_ads_mcp.client import request
from openai_ads_mcp.coordinator import mcp


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_ads(
    ad_group_id: str,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    order: Optional[str] = None,
) -> Any:
    """List ads for an ad group."""
    return request(
        "GET",
        "/ads",
        params={
            "ad_group_id": ad_group_id,
            "limit": limit,
            "after": after,
            "before": before,
            "order": order,
        },
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_ad(ad_id: str) -> Any:
    """Fetch one ad by id."""
    return request("GET", f"/ads/{ad_id}")
