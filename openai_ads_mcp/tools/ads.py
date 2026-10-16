"""Ad creative / placement tools: read and write."""

from typing import Any, Mapping, Optional

from mcp.types import ToolAnnotations

from openai_ads_mcp.client import request
from openai_ads_mcp.coordinator import mcp


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_ads(ad_group_id: str, limit: Optional[int] = None, after: Optional[str] = None, before: Optional[str] = None, order: Optional[str] = None) -> Any:
    """List ads for an ad group."""
    return request("GET", "/ads", params={"ad_group_id": ad_group_id, "limit": limit, "after": after, "before": before, "order": order})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_ad(ad_id: str) -> Any:
    """Fetch one ad by id."""
    return request("GET", f"/ads/{ad_id}")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def create_ad(ad_group_id: str, name: str, creative: Mapping[str, Any], status: str = "paused") -> Any:
    """Create an ad. New ads default to paused.

    creative must contain type, title and body. chat_card creatives also need
    target_url and usually file_id.
    """
    if status not in ("active", "paused"):
        raise ValueError("status must be 'active' or 'paused' on create.")
    required = ("type", "title", "body")
    missing = [key for key in required if not creative.get(key)]
    if missing:
        raise ValueError(f"creative is missing required fields: {', '.join(missing)}")
    if creative.get("type") == "chat_card" and not creative.get("target_url"):
        raise ValueError("chat_card creative requires target_url.")
    return request("POST", "/ads", json_body={"ad_group_id": ad_group_id, "name": name, "status": status, "creative": dict(creative)})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def update_ad(ad_id: str, name: Optional[str] = None, status: Optional[str] = None, creative: Optional[Mapping[str, Any]] = None) -> Any:
    """Update an ad. If creative is provided, send the complete creative object."""
    if status is not None and status not in ("active", "paused", "archived"):
        raise ValueError("status must be 'active', 'paused', or 'archived'.")
    return request("POST", f"/ads/{ad_id}", json_body={"name": name, "status": status, "creative": dict(creative) if creative is not None else None})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def activate_ad(ad_id: str) -> Any:
    """Activate an ad."""
    return request("POST", f"/ads/{ad_id}/activate")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def pause_ad(ad_id: str) -> Any:
    """Pause an ad."""
    return request("POST", f"/ads/{ad_id}/pause")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
def archive_ad(ad_id: str) -> Any:
    """Archive an ad. This is not reversible."""
    return request("POST", f"/ads/{ad_id}/archive")
