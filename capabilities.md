# OpenAI ChatGPT Ads MCP — capabilities reference

This document describes the Model Context Protocol server for the OpenAI
ChatGPT **Ads API** (`OpenAI Ads Server` in FastMCP): tools an agent can call,
parameters, and notes. Official reference:
[Ads API](https://developers.openai.com/ads/api-reference/authentication).

**Authentication:** set `OPENAI_ADS_API_KEY`; requests use
`Authorization: Bearer <key>` against `https://api.ads.openai.com/v1`.

**Current surface:** only read/list/report tools are registered — **GET**
operations equivalent below. Create/update/state-change actions and file uploads
are **not** exposed until explicitly re-added.

All registered tools use MCP annotations **`readOnlyHint: true`**.

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

---

## Ad groups

### `list_ad_groups`

- `campaign_id` (required)
- Optional: `limit`, `after`, `before`, `order`
  [Ad groups](https://developers.openai.com/ads/api-reference/ad-groups)

### `get_ad_group`

- `ad_group_id`

---

## Ads

### `list_ads`

- `ad_group_id` (required)
- Optional: `limit`, `after`, `before`, `order`
  [Ads](https://developers.openai.com/ads/api-reference/ads)

### `get_ad`

- `ad_id`

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
