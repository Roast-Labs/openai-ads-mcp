"""Campaign tools: read and write.

Read tools: list_campaigns, get_campaign.
Write tools: create_campaign, update_campaign, activate_campaign,
pause_campaign, archive_campaign, duplicate_campaign.

Safety defaults:
- New campaigns are created with status "paused" unless explicitly set.
- A lifetime spend limit is required and must be at least 1 EUR
  (1,000,000 micros), matching the API minimum.
- archive_campaign is irreversible and is marked as destructive.

API reference: https://developers.openai.com/ads/api-reference/campaigns
"""

from typing import Any, Mapping, Optional

from mcp.types import ToolAnnotations

from openai_ads_mcp.client import request
from openai_ads_mcp.coordinator import mcp

_MIN_LIFETIME_SPEND_MICROS = 1_000_000  # 1 EUR, API minimum


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


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def create_campaign(
    name: str,
    lifetime_spend_limit_micros: int,
    status: str = "paused",
    description: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    bidding_type: Optional[str] = None,
    conversion_event_setting_ids: Optional[list[str]] = None,
    targeting: Optional[Mapping[str, Any]] = None,
    mode: Optional[str] = None,
) -> Any:
    """Create a campaign in the current ad account.

    Defaults to status "paused" so nothing spends until it is activated.
    lifetime_spend_limit_micros is required: 1 EUR = 1000000 micros, minimum 1 EUR.
    bidding_type: impressions (default), clicks, or conversions.
    start_time / end_time: Unix timestamps (seconds).
    targeting example: {"locations": {"include": [{"id": "1000056"}]}}
    (1000056 = Germany).

    See https://developers.openai.com/ads/api-reference/campaigns
    """
    if status not in ("active", "paused"):
        raise ValueError("status must be 'active' or 'paused' on create.")
    if lifetime_spend_limit_micros < _MIN_LIFETIME_SPEND_MICROS:
        raise ValueError("lifetime_spend_limit_micros must be at least 1000000 (1 EUR).")
    if bidding_type == "conversions" and not conversion_event_setting_ids:
        raise ValueError("bidding_type 'conversions' requires conversion_event_setting_ids.")

    body = {
        "name": name,
        "status": status,
        "budget": {"lifetime_spend_limit_micros": lifetime_spend_limit_micros},
        "description": description,
        "start_time": start_time,
        "end_time": end_time,
        "bidding_type": bidding_type,
        "conversion_event_setting_ids": conversion_event_setting_ids,
        "targeting": dict(targeting) if targeting is not None else None,
        "mode": mode,
    }
    return request("POST", "/campaigns", json_body=body)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def update_campaign(
    campaign_id: str,
    status: Optional[str] = None,
    description: Optional[str] = None,
    lifetime_spend_limit_micros: Optional[int] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    targeting: Optional[Mapping[str, Any]] = None,
) -> Any:
    """Update a campaign. Only the fields you pass are changed.

    status: active, paused, or archived (prefer the dedicated activate, pause,
    archive tools). bidding_type cannot be changed.
    lifetime_spend_limit_micros: sent as the full budget object; minimum 1000000.

    See https://developers.openai.com/ads/api-reference/campaigns
    """
    if status is not None and status not in ("active", "paused", "archived"):
        raise ValueError("status must be 'active', 'paused', or 'archived'.")
    if lifetime_spend_limit_micros is not None and lifetime_spend_limit_micros < _MIN_LIFETIME_SPEND_MICROS:
        raise ValueError("lifetime_spend_limit_micros must be at least 1000000 (1 EUR).")

    body = {
        "status": status,
        "description": description,
        "budget": (
            {"lifetime_spend_limit_micros": lifetime_spend_limit_micros}
            if lifetime_spend_limit_micros is not None
            else None
        ),
        "start_time": start_time,
        "end_time": end_time,
        "targeting": dict(targeting) if targeting is not None else None,
    }
    return request("POST", f"/campaigns/{campaign_id}", json_body=body)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def activate_campaign(campaign_id: str) -> Any:
    """Activate a campaign so it starts delivering ads (spends budget).

    See https://developers.openai.com/ads/api-reference/campaigns
    """
    return request("POST", f"/campaigns/{campaign_id}/activate")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def pause_campaign(campaign_id: str) -> Any:
    """Pause a campaign. Paused campaigns do not deliver ads.

    See https://developers.openai.com/ads/api-reference/campaigns
    """
    return request("POST", f"/campaigns/{campaign_id}/pause")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True))
def archive_campaign(campaign_id: str) -> Any:
    """Archive a campaign. This is NOT reversible. Only use when the campaign is no longer needed.

    See https://developers.openai.com/ads/api-reference/campaigns
    """
    return request("POST", f"/campaigns/{campaign_id}/archive")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def duplicate_campaign(
    source_campaign_id: str,
    name: str,
    lifetime_spend_limit_micros: int,
    bidding_type: str = "conversions",
    conversion_event_setting_ids: Optional[list[str]] = None,
    max_bid_micros: Optional[int] = None,
) -> Any:
    """Duplicate a campaign with its ad groups and ads, all paused.

    The source campaign's targeting, description, dates and conversion events
    are copied. bidding_type defaults to conversions. A lifetime budget is
    required because the Ads API does not create campaigns from daily budgets.
    """
    if lifetime_spend_limit_micros < _MIN_LIFETIME_SPEND_MICROS:
        raise ValueError("lifetime_spend_limit_micros must be at least 1000000 (1 EUR).")
    if bidding_type not in ("impressions", "clicks", "conversions"):
        raise ValueError("bidding_type must be 'impressions', 'clicks', or 'conversions'.")

    source = request("GET", f"/campaigns/{source_campaign_id}")
    events = conversion_event_setting_ids
    if events is None:
        events = source.get("conversion_event_setting_ids") or []
    if bidding_type == "conversions" and not events:
        raise ValueError("Conversion campaigns require conversion_event_setting_ids.")

    campaign_body = {
        "name": name,
        "description": source.get("description"),
        "start_time": source.get("start_time"),
        "end_time": source.get("end_time"),
        "status": "paused",
        "budget": {"lifetime_spend_limit_micros": lifetime_spend_limit_micros},
        "bidding_type": bidding_type,
        "conversion_event_setting_ids": events,
        "targeting": source.get("targeting"),
        "mode": source.get("mode"),
    }
    created_campaign = request("POST", "/campaigns", json_body=campaign_body)
    new_campaign_id = created_campaign["id"]

    copied_groups = []
    copied_ads = []
    groups = request("GET", "/ad_groups", params={"campaign_id": source_campaign_id})
    for source_group in groups.get("data", []):
        source_bid = (source_group.get("bidding_config") or {}).get("max_bid_micros")
        bid = max_bid_micros if max_bid_micros is not None else source_bid
        if bid is None:
            raise ValueError(f"Source ad group {source_group.get('id')} has no max_bid_micros.")
        billing_event = "click" if bidding_type == "conversions" else (source_group.get("bidding_config") or {}).get("billing_event_type", "impression")
        new_group = request("POST", "/ad_groups", json_body={
            "campaign_id": new_campaign_id,
            "name": source_group.get("name"),
            "description": source_group.get("description"),
            "context_hints": source_group.get("context_hints"),
            "status": "paused",
            "bidding_config": {"billing_event_type": billing_event, "max_bid_micros": bid},
        })
        copied_groups.append(new_group)

        ads = request("GET", "/ads", params={"ad_group_id": source_group["id"]})
        for source_ad in ads.get("data", []):
            creative = source_ad.get("creative")
            if not creative:
                raise ValueError(f"Source ad {source_ad.get('id')} has no creative data.")
            new_ad = request("POST", "/ads", json_body={
                "ad_group_id": new_group["id"],
                "name": source_ad.get("name"),
                "status": "paused",
                "creative": creative,
            })
            copied_ads.append(new_ad)

    return {
        "campaign": created_campaign,
        "ad_groups": copied_groups,
        "ads": copied_ads,
        "status": "paused",
    }
