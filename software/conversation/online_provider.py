"""Online AI provider adapter (optional, requires internet).

This adapter is backend-neutral. The actual HTTP client is injected so no
vendor SDK is hard-coded and no network call happens in tests. API keys
are read from the environment by the caller and passed in; they are never
hard-coded or logged here.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from .base import ConversationError, ConversationProvider, Message


class OnlineProvider(ConversationProvider):
    name = "online"
    requires_internet = True

    def __init__(
        self,
        client: Optional[Callable[[List[Message]], str]] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self._client = client
        self._has_key = bool(api_key)

    def available(self) -> bool:
        return self._client is not None and self._has_key

    def generate(self, messages: List[Message]) -> str:
        if not self.available():
            raise ConversationError("online provider unavailable (missing client or API key)")
        try:
            out = self._client(messages)  # type: ignore[misc]
        except Exception as exc:  # noqa: BLE001
            raise ConversationError(f"online provider request failed: {exc}") from exc
        if not isinstance(out, str):
            raise ConversationError("online provider must return str")
        return out
