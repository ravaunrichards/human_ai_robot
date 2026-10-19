"""Local language-model provider adapter (offline-capable).

This is a hardware-neutral adapter. It is wired to call a local model
runner (e.g. llama.cpp / Ollama / a local HTTP endpoint) through an
injected callable so the actual backend can be swapped without changing
this file. If no backend is configured it reports itself unavailable so
the manager falls back to the EchoProvider.

No model weights are bundled. See docs/system_architecture/ai_architecture.md.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from .base import ConversationError, ConversationProvider, Message


class LocalLLMProvider(ConversationProvider):
    name = "local"
    requires_internet = False

    def __init__(self, runner: Optional[Callable[[List[Message]], str]] = None) -> None:
        # runner(messages) -> str. None means no local model is installed.
        self._runner = runner

    def available(self) -> bool:
        return self._runner is not None

    def generate(self, messages: List[Message]) -> str:
        if self._runner is None:
            raise ConversationError("no local model runner configured")
        try:
            out = self._runner(messages)
        except Exception as exc:  # noqa: BLE001
            raise ConversationError(f"local model runner failed: {exc}") from exc
        if not isinstance(out, str):
            raise ConversationError("local model runner must return str")
        return out
