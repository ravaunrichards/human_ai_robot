"""Speech-to-text interface."""

from __future__ import annotations

import abc
from typing import Optional


class STTError(RuntimeError):
    pass


class SpeechToText(abc.ABC):
    name = "base-stt"
    requires_internet = False

    @abc.abstractmethod
    def transcribe(self, pcm16: bytes, sample_rate: int = 16000) -> str:
        ...

    def available(self) -> bool:
        return True


class NullSTT(SpeechToText):
    """Offline no-op STT used for development/tests.

    Returns an empty transcription and marks itself unavailable so higher
    layers can detect that no real engine is installed.
    """

    name = "null-stt"

    def available(self) -> bool:
        return False

    def transcribe(self, pcm16: bytes, sample_rate: int = 16000) -> str:
        if not isinstance(pcm16, (bytes, bytearray)):
            raise STTError("pcm16 must be bytes")
        return ""
