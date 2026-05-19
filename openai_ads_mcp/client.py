"""HTTP client for the OpenAI ChatGPT Ads API.

Base URL and bearer auth per
https://developers.openai.com/ads/api-reference/authentication
"""

from __future__ import annotations

import os
from typing import Any, Mapping, Optional, Sequence, Union

import httpx
from dotenv import load_dotenv

load_dotenv()

_BASE_URL = "https://api.ads.openai.com/v1"
_DEFAULT_TIMEOUT_SECONDS = 60.0


class OpenAIAdsError(RuntimeError):
    """Raised when the Ads API returns an error or the client is misconfigured."""


def _require_api_key() -> str:
    key = os.environ.get("OPENAI_ADS_API_KEY")
    if not key:
        raise OpenAIAdsError(
            "OPENAI_ADS_API_KEY is not set. Use an Ads API key from your OpenAI "
            "developer account and expose it as OPENAI_ADS_API_KEY "
            "(Authorization: Bearer … per "
            "https://developers.openai.com/ads/api-reference/authentication)."
        )
    return key


def _build_client() -> httpx.Client:
    return httpx.Client(
        base_url=_BASE_URL,
        headers={
            "Authorization": f"Bearer {_require_api_key()}",
            "Accept": "application/json",
        },
        timeout=httpx.Timeout(_DEFAULT_TIMEOUT_SECONDS),
    )


def _drop_nulls(data: Optional[Mapping[str, Any]]) -> Optional[dict]:
    if data is None:
        return None
    return {k: v for k, v in data.items() if v is not None}


ParamsInput = Union[Mapping[str, Any], Sequence[tuple[str, str]], None]


def request(
    method: str,
    path: str,
    *,
    params: ParamsInput = None,
    json_body: Optional[Mapping[str, Any]] = None,
) -> Any:
    """Perform an Ads API request with JSON body or query params."""
    kwargs: dict[str, Any] = {}
    if isinstance(params, Sequence) and not isinstance(params, (str, bytes)):
        kwargs["params"] = list(params)
    elif params is not None:
        kwargs["params"] = _drop_nulls(dict(params))

    if json_body is not None:
        kwargs["json"] = _drop_nulls(dict(json_body))

    with _build_client() as client:
        response = client.request(method, path, **kwargs)

    if response.is_error:
        raise OpenAIAdsError(
            f"Ads API error {response.status_code} for {method} {path}: "
            f"{response.text}"
        )

    if not response.content:
        return {"status": response.status_code}

    content_type = response.headers.get("content-type", "")
    if "json" in content_type.lower():
        return response.json()
    return response.text
