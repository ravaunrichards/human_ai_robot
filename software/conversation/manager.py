"""Conversation manager with provider fallback.

Chooses the configured provider, and transparently falls back to the
next available provider (ending at the always-available EchoProvider) if
a provider is unavailable or raises. This guarantees the robot keeps a
conversational response path even when internet or a local model fails.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

from .base import ConversationError, ConversationProvider, Message
from .echo_provider import EchoProvider


class ConversationManager:
    def __init__(self, providers: Sequence[ConversationProvider], history_limit: int = 50) -> None:
        provs = list(providers)
        if not any(isinstance(p, EchoProvider) for p in provs):
            provs.append(EchoProvider())  # guaranteed offline fallback
        self._providers = provs
        self._history: List[Message] = []
        self._history_limit = history_limit
        self.last_provider: Optional[str] = None
        self.last_fell_back: bool = False

    def add_system(self, content: str) -> None:
        self._history.insert(0, Message("system", content))

    def reply(self, user_text: str) -> str:
        self._history.append(Message("user", user_text))
        self._trim()
        self.last_fell_back = False
        errors = []
        for i, provider in enumerate(self._providers):
            if not provider.available():
                errors.append(f"{provider.name}: unavailable")
                continue
            try:
                out = provider.generate(list(self._history))
                self._history.append(Message("assistant", out))
                self._trim()
                self.last_provider = provider.name
                self.last_fell_back = i > 0
                return out
            except ConversationError as exc:
                errors.append(f"{provider.name}: {exc}")
                continue
        raise ConversationError("all providers failed: " + "; ".join(errors))

    def _trim(self) -> None:
        system = [m for m in self._history if m.role == "system"]
        rest = [m for m in self._history if m.role != "system"]
        if len(rest) > self._history_limit:
            rest = rest[-self._history_limit :]
        self._history = system + rest

    @property
    def history(self) -> List[Message]:
        return list(self._history)
