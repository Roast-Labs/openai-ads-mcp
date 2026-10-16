# OpenAI ChatGPT Ads MCP — capabilities reference

This document describes the Model Context Protocol server for the OpenAI
ChatGPT **Ads API** (`OpenAI Ads Server` in FastMCP): tools an agent can call,
parameters, and notes. Official reference:
[Ads API](https://developers.openai.com/ads/api-reference/authentication).

**Authentication:** set `OPENAI_ADS_API_KEY`; requests use
`Authorization: Bearer <key>` against `https://api.ads.openai.com/v1`.

**Current surface:** read/list/report tools plus write and state-change tools are registered. New campaigns, ad groups, and ads default to `paused`; archive actions are destructive.

Write tools use MCP annotations with **`readOnlyHint: false`**. Read tools remain annotated with **`readOnlyHint: true`**.

---

## Ad account

### `get_ad_account`

`GET /ad_account` — metadata for the current account (id, name, urls, timezone,
currency).
[Ad account](https://developers.openai.com/ads/api-reference/ad-account)

---

## Campaigns

### `list_campaigns`

Optional: `limit`, `after`, `before`, `order` (`asc` | `desc`).
[Campaigns](https://developers.openai.com/ads/api-reference/campaigns)

### `get_campaign`

- `campaign_id` (string)

### Campaign write tools

- `create_campaign`: creates a paused campaign by default; requires `name` and `lifetime_spend_limit_micros`.
- `update_campaign`: updates campaign fields and budget.
- `activate_campaign`, `pause_campaign`, `archive_campaign`: change campaign state.
- `duplicate_campaign`: copies a campaign, its ad groups, and ads. The copies remain paused and require a lifetime budget (`lifetime_spend_limit_micros`). `bidding_type` defaults to `conversions`; `max_bid_micros` optionally overrides the bid of the copied ad groups.

---

## Ad groups

### `list_ad_groups`

- `campaign_id` (required)
- Optional: `limit`, `after`, `before`, `order`
  [Ad groups](https://developers.openai.com/ads/api-reference/ad-groups)

### `get_ad_group`

- `ad_group_id`

### Ad-group write tools

- `create_ad_group`: creates a paused ad group by default.
- `update_ad_group`: updates ad-group fields.
- `activate_ad_group`, `pause_ad_group`, `archive_ad_group`: change ad-group state.

---

## Ads

### `list_ads`

- `ad_group_id` (required)
- Optional: `limit`, `after`, `before`, `order`
  [Ads](https://developers.openai.com/ads/api-reference/ads)

### `get_ad`

- `ad_id`

### Ad write tools

- `create_ad`: creates a paused ad by default and requires creative data.
- `update_ad`: updates name, status, or creative.
- `activate_ad`, `pause_ad`, `archive_ad`: change ad state.

---

## Insights

Each tool builds query parameters; array-style arguments use repeated keys
(`fields[]`, `time_ranges[]`, `filters[]`, `sort[]`) like the official curl
examples.

Optional on all four: `time_granularity`, `aggregation_level`, `limit`, `before`,
`after`, `time_ranges`, `filters`, `fields`, `sort` (lists of strings). For
object-valued entries (e.g. `time_ranges`, `sort`), pass JSON-encoded strings per
row.
[Insights](https://developers.openai.com/ads/api-reference/insights)

### `get_ad_account_insights`

`GET /ad_account/insights`

### `get_campaign_insights`

- `campaign_id` + optional insight params above.

### `get_ad_group_insights`

- `ad_group_id` + optional insight params.

### `get_ad_insights`

- `ad_id` + optional insight params.

---

## Official documentation

- [Authentication & base URL](https://developers.openai.com/ads/api-reference/authentication)
- [Campaigns](https://developers.openai.com/ads/api-reference/campaigns)
- [Ad groups](https://developers.openai.com/ads/api-reference/ad-groups)
- [Ads](https://developers.openai.com/ads/api-reference/ads)
- [Insights](https://developers.openai.com/ads/api-reference/insights)
