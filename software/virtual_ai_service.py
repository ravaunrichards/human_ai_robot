"""Strict, shared conversation service for the browser-based virtual robot.

Unlike the legacy developer loop, this service never falls back to EchoProvider.
If a real model is not configured or its request fails, it raises an explicit
error rather than presenting a canned response as an AI-generated answer.
"""
from __future__ import annotations

import json
import os
import threading
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass(frozen=True)
class Message:
    role: str
    content: str


DEFAULT_SYSTEM_PROMPT = (
    "You are the conversational intelligence for human_ai_robot, a virtual AI "
    "companion connected to a humanoid robotics engineering project. Be helpful, "
    "honest, warm, and clear. You are currently running in software simulation "
    "only: you have no physical body, no live camera or microphone access unless "
    "a capability is explicitly connected, and you cannot move real motors. "
    "Never claim a physical action or sensor observation occurred when it did not. "
    "When asked about robotics, prioritise safety and distinguish implemented "
    "features from proposed features."
)


class VirtualAIError(RuntimeError):
    """Base error suitable for reporting a safe, user-facing service problem."""


class AINotConfigured(VirtualAIError):
    """Raised when no real model credentials are configured."""


class AIProviderFailure(VirtualAIError):
    """Raised when the real model provider fails or returns invalid data."""


def _openai_compatible_request(
    messages: List[Message],
    *,
    api_key: str,
    model: str,
    base_url: str,
    timeout_seconds: float = 60.0,
) -> str:
    """Call an OpenAI-compatible Chat Completions endpoint using the stdlib."""
    endpoint = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": item.role, "content": item.content} for item in messages],
        "max_completion_tokens": 800,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "human-ai-robot/virtual-ai",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            response_body = response.read(2_000_000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        # Do not return request headers or the API key in diagnostics.
        try:
            body = exc.read(4000).decode("utf-8", errors="replace")
            data = json.loads(body) if body else {}
            detail = data.get("error", {}).get("message", "") if isinstance(data, dict) else ""
        except Exception:  # noqa: BLE001
            detail = ""
        detail = str(detail).strip()[:500]
        suffix = (": " + detail) if detail else ""
        raise AIProviderFailure("AI provider returned HTTP %s%s" % (exc.code, suffix)) from None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        # The exception text can contain host information but never the secret.
        reason = getattr(exc, "reason", None)
        description = str(reason or exc.__class__.__name__)[:300]
        raise AIProviderFailure("Could not reach the AI provider: " + description) from None

    try:
        data = json.loads(response_body)
        choices = data["choices"]
        content = choices[0]["message"]["content"]
    except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise AIProviderFailure("AI provider returned an unrecognised response format") from exc
    if not isinstance(content, str) or not content.strip():
        raise AIProviderFailure("AI provider returned an empty response")
    return content.strip()


class VirtualAIService:
    """One conversation shared by every browser connected to this server."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        system_prompt: Optional[str] = None,
        request_fn: Optional[Callable[[List[Message]], str]] = None,
        history_limit: int = 40,
    ) -> None:
        self.api_key = (os.environ.get("OPENAI_API_KEY", "") if api_key is None else api_key).strip()
        self.model = (model or os.environ.get("OPENAI_MODEL") or "gpt-5.5").strip()
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1").strip().rstrip("/")
        self._lock = threading.RLock()
        self._history_limit = max(4, int(history_limit))
        self._history: List[Message] = [
            Message("system", system_prompt or os.environ.get("ROBOT_AI_SYSTEM_PROMPT") or DEFAULT_SYSTEM_PROMPT)
        ]
        if request_fn is not None and self.api_key:
            self._request_fn = request_fn
        elif self.api_key:
            self._request_fn = lambda messages: _openai_compatible_request(
                messages,
                api_key=self.api_key,
                model=self.model,
                base_url=self.base_url,
            )
        else:
            self._request_fn = None

    def status(self) -> Dict[str, object]:
        with self._lock:
            return {
                "service": "human_ai_robot",
                "ai_configured": self._request_fn is not None,
                "provider": "OpenAI-compatible Chat Completions" if self._request_fn else "Not configured",
                "model": self.model if self._request_fn else None,
                "conversation_messages": sum(1 for item in self._history if item.role in ("user", "assistant")),
                "simulation_only": True,
                "motion_control": "disabled",
                "reply_fallback": False,
            }

    def history(self) -> List[Dict[str, str]]:
        with self._lock:
            return [
                {"role": item.role, "content": item.content}
                for item in self._history
                if item.role in ("user", "assistant")
            ]

    def reply(self, text: str) -> str:
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        if len(cleaned) > 4000:
            raise ValueError("Message is too long; limit is 4,000 characters.")
        if self._request_fn is None:
            raise AINotConfigured(
                "No real AI model is configured. Set OPENAI_API_KEY on the server and restart it. "
                "This interface deliberately does not generate demo or echo replies."
            )

        # Serialise calls so two devices cannot race each other and see divergent turns.
        with self._lock:
            candidate = [self._history[0]] + self._history[1:]
            candidate.append(Message("user", cleaned))
            try:
                answer = self._request_fn(candidate)
            except VirtualAIError:
                raise
            except Exception as exc:  # noqa: BLE001
                raise AIProviderFailure("AI provider request failed: " + exc.__class__.__name__) from None
            if not isinstance(answer, str) or not answer.strip():
                raise AIProviderFailure("The AI provider returned no text.")
            self._history = candidate + [Message("assistant", answer.strip())]
            non_system = self._history[1:]
            if len(non_system) > self._history_limit:
                non_system = non_system[-self._history_limit :]
            self._history = [self._history[0]] + non_system
            return answer.strip()

    def clear_history(self) -> None:
        with self._lock:
            self._history = [self._history[0]]
