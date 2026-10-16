"""Bearer token authentication for the HTTP transport."""

from __future__ import annotations

import hmac
import os

AUTH_TOKEN_ENV = "MCP_AUTH_TOKEN"


def get_auth_token() -> str | None:
    """Return the configured bearer token, or None if unset/empty."""
    token = os.environ.get(AUTH_TOKEN_ENV, "").strip()
    return token or None


class BearerAuthMiddleware:
    """Pure ASGI middleware requiring ``Authorization: Bearer <token>``."""

    def __init__(self, app, token: str) -> None:
        self.app = app
        self._token = token.encode("utf-8")

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] == "lifespan":
            await self.app(scope, receive, send)
            return

        if scope["type"] == "http" and self._authorized(scope):
            await self.app(scope, receive, send)
            return

        if scope["type"] == "http":
            body = b'{"error":"unauthorized"}'
            await send(
                {
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (b"content-length", str(len(body)).encode()),
                        (b"www-authenticate", b"Bearer"),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
        elif scope["type"] == "websocket":
            await send({"type": "websocket.close", "code": 1008})

    def _authorized(self, scope) -> bool:
        auth = b""
        for name, value in scope.get("headers", []):
            if name == b"authorization":
                auth = value
                break
        scheme, _, credential = auth.partition(b" ")
        if scheme.lower() != b"bearer":
            return False
        return hmac.compare_digest(credential.strip(), self._token)
