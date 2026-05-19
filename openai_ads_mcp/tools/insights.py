"""Reporting / insights tools.

Query array parameters use repeated keys (e.g. fields[], time_ranges[]) as in
https://developers.openai.com/ads/api-reference/insights
"""

from __future__ import annotations

from typing import Any, Optional

from mcp.types import ToolAnnotations

from openai_ads_mcp.client import request
from openai_ads_mcp.coordinator import mcp


def _insights_params(
    *,
    time_granularity: Optional[str] = None,
    aggregation_level: Optional[str] = None,
    limit: Optional[int] = None,
    before: Optional[str] = None,
    after: Optional[str] = None,
    time_ranges: Optional[list[str]] = None,
    filters: Optional[list[str]] = None,
    fields: Optional[list[str]] = None,
    sort: Optional[list[str]] = None,
) -> list[tuple[str, str]]:
    """Build query pairs for repeated `[]` style parameters."""
    out: list[tuple[str, str]] = []
    if time_granularity is not None:
        out.append(("time_granularity", time_granularity))
    if aggregation_level is not None:
        out.append(("aggregation_level", aggregation_level))
    if limit is not None:
        out.append(("limit", str(limit)))
    if before is not None:
        out.append(("before", before))
    if after is not None:
        out.append(("after", after))
    for item in time_ranges or []:
        out.append(("time_ranges[]", item))
    for item in filters or []:
        out.append(("filters[]", item))
    for item in fields or []:
        out.append(("fields[]", item))
    for item in sort or []:
        out.append(("sort[]", item))
    return out


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_ad_account_insights(
    time_granularity: Optional[str] = None,
    aggregation_level: Optional[str] = None,
    limit: Optional[int] = None,
    before: Optional[str] = None,
    after: Optional[str] = None,
    time_ranges: Optional[list[str]] = None,
    filters: Optional[list[str]] = None,
    fields: Optional[list[str]] = None,
    sort: Optional[list[str]] = None,
) -> Any:
    """GET /ad_account/insights — account-scoped reporting rows.

    Pass `time_ranges`, `filters`, `fields`, and `sort` entries as JSON strings
    when the API expects objects (see official curl examples).
    """
    return request(
        "GET",
        "/ad_account/insights",
        params=_insights_params(
            time_granularity=time_granularity,
            aggregation_level=aggregation_level,
            limit=limit,
            before=before,
            after=after,
            time_ranges=time_ranges,
            filters=filters,
            fields=fields,
            sort=sort,
        ),
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_campaign_insights(
    campaign_id: str,
    time_granularity: Optional[str] = None,
    aggregation_level: Optional[str] = None,
    limit: Optional[int] = None,
    before: Optional[str] = None,
    after: Optional[str] = None,
    time_ranges: Optional[list[str]] = None,
    filters: Optional[list[str]] = None,
    fields: Optional[list[str]] = None,
    sort: Optional[list[str]] = None,
) -> Any:
    """GET /campaigns/{campaign_id}/insights."""
    return request(
        "GET",
        f"/campaigns/{campaign_id}/insights",
        params=_insights_params(
            time_granularity=time_granularity,
            aggregation_level=aggregation_level,
            limit=limit,
            before=before,
            after=after,
            time_ranges=time_ranges,
            filters=filters,
            fields=fields,
            sort=sort,
        ),
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_ad_group_insights(
    ad_group_id: str,
    time_granularity: Optional[str] = None,
    aggregation_level: Optional[str] = None,
    limit: Optional[int] = None,
    before: Optional[str] = None,
    after: Optional[str] = None,
    time_ranges: Optional[list[str]] = None,
    filters: Optional[list[str]] = None,
    fields: Optional[list[str]] = None,
    sort: Optional[list[str]] = None,
) -> Any:
    """GET /ad_groups/{ad_group_id}/insights."""
    return request(
        "GET",
        f"/ad_groups/{ad_group_id}/insights",
        params=_insights_params(
            time_granularity=time_granularity,
            aggregation_level=aggregation_level,
            limit=limit,
            before=before,
            after=after,
            time_ranges=time_ranges,
            filters=filters,
            fields=fields,
            sort=sort,
        ),
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_ad_insights(
    ad_id: str,
    time_granularity: Optional[str] = None,
    aggregation_level: Optional[str] = None,
    limit: Optional[int] = None,
    before: Optional[str] = None,
    after: Optional[str] = None,
    time_ranges: Optional[list[str]] = None,
    filters: Optional[list[str]] = None,
    fields: Optional[list[str]] = None,
    sort: Optional[list[str]] = None,
) -> Any:
    """GET /ads/{ad_id}/insights."""
    return request(
        "GET",
        f"/ads/{ad_id}/insights",
        params=_insights_params(
            time_granularity=time_granularity,
            aggregation_level=aggregation_level,
            limit=limit,
            before=before,
            after=after,
            time_ranges=time_ranges,
            filters=filters,
            fields=fields,
            sort=sort,
        ),
    )
