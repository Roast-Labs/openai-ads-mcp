"""Ad group tools: read and write."""

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


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def create_ad_group(
    campaign_id: str,
    name: str,
    max_bid_micros: int,
    status: str = "paused",
    description: Optional[str] = None,
    context_hints: Optional[list[str]] = None,
    billing_event_type: str = "click",
) -> Any:
    """Create an ad group. New ad groups default to paused."""
    if status not in ("active", "paused"):
        raise ValueError("status must be 'active' or 'paused' on create.")
    if billing_event_type not in ("impression", "click"):
        raise ValueError("billing_event_type must be 'impression' or 'click'.")
    if max_bid_micros < 1:
        raise ValueError("max_bid_micros must be at least 1.")
    return request(
        "POST",
        "/ad_groups",
        json_body={
            "campaign_id": campaign_id,
            "name": name,
            "description": description,
            "context_hints": context_hints,
            "status": status,
            "bidding_config": {
                "billing_event_type": billing_event_type,
                "max_bid_micros": max_bid_micros,
            },
        },
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def update_ad_group(
    ad_group_id: str,
    status: Optional[str] = None,
    description: Optional[str] = None,
    context_hints: Optional[list[str]] = None,
    max_bid_micros: Optional[int] = None,
    billing_event_type: Optional[str] = None,
) -> Any:
    """Update an ad group. Only provided fields are changed."""
    if status is not None and status not in ("active", "paused", "archived"):
        raise ValueError("status must be 'active', 'paused', or 'archived'.")
    if max_bid_micros is not None and max_bid_micros < 1:
        raise ValueError("max_bid_micros must be at least 1.")
    if billing_event_type is not None and billing_event_type not in ("impression", "click"):
        raise ValueError("billing_event_type must be 'impression' or 'click'.")
    bidding_config = None
    if max_bid_micros is not None or billing_event_type is not None:
        bidding_config = {
            "max_bid_micros": max_bid_micros,
            "billing_event_type": billing_event_type,
        }
    return request(
        "POST",
        f"/ad_groups/{ad_group_id}",
        json_body={
            "status": status,
            "description": description,
            "context_hints": context_hints,
            "bidding_config": bidding_config,
        },
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def activate_ad_group(ad_group_id: str) -> Any:
    """Activate an ad group."""
    return request("POST", f"/ad_groups/{ad_group_id}/activate")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def pause_ad_group(ad_group_id: str) -> Any:
    """Pause an ad group."""
    return request("POST", f"/ad_groups/{ad_group_id}/pause")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
def archive_ad_group(ad_group_id: str) -> Any:
    """Archive an ad group. This is not reversible."""
    return request("POST", f"/ad_groups/{ad_group_id}/archive")
