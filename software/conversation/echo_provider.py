"""A trivial offline provider used for tests and development.

It never needs internet and simply echoes a canned, deterministic reply.
Useful as the guaranteed offline fallback.
"""

from __future__ import annotations

from typing import List

from .base import ConversationProvider, Message


class EchoProvider(ConversationProvider):
    name = "echo"
    requires_internet = False

    def generate(self, messages: List[Message]) -> str:
        last_user = next((m for m in reversed(messages) if m.role == "user"), None)
        if last_user is None:
            return "(no user message)"
        return f"[offline-echo] {last_user.content.strip()}"
