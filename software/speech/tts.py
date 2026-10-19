"""Text-to-speech interface."""

from __future__ import annotations

import abc


class TTSError(RuntimeError):
    pass


class TextToSpeech(abc.ABC):
    name = "base-tts"
    requires_internet = False

    @abc.abstractmethod
    def synthesize(self, text: str, sample_rate: int = 22050) -> bytes:
        """Return PCM16 mono audio bytes for ``text``."""

    def available(self) -> bool:
        return True


class NullTTS(TextToSpeech):
    """Offline no-op TTS: returns silence of a length proportional to text."""

    name = "null-tts"

    def available(self) -> bool:
        return False

    def synthesize(self, text: str, sample_rate: int = 22050) -> bytes:
        if not isinstance(text, str):
            raise TTSError("text must be a string")
        # ~60 ms of silence per character, capped.
        n_samples = min(len(text), 500) * int(sample_rate * 0.06)
        return b"\x00\x00" * n_samples
