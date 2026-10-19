"""Conversation provider interface.

Providers are replaceable adapters. The ONLY contract they must satisfy
is :meth:`generate`. Providers must never return motor commands; they
return text. Any motion must be produced by the motion planner from a
bounded intention, not from raw provider output.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import List


class ConversationError(RuntimeError):
    pass


@dataclass
class Message:
    role: str  # "system" | "user" | "assistant"
    content: str

    def __post_init__(self) -> None:
        if self.role not in ("system", "user", "assistant"):
            raise ValueError(f"invalid role: {self.role}")
        if not isinstance(self.content, str):
            raise ValueError("content must be a string")


class ConversationProvider(abc.ABC):
    name: str = "base"
    requires_internet: bool = False

    @abc.abstractmethod
    def generate(self, messages: List[Message]) -> str:
        """Return an assistant reply for the given conversation."""

    def available(self) -> bool:
        """Return True if the provider can currently serve requests."""
        return True
