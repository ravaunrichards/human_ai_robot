"""Audio device interface (capture / playback)."""

from __future__ import annotations

import abc


class AudioDevice(abc.ABC):
    @abc.abstractmethod
    def read(self, n_frames: int) -> bytes:
        ...

    @abc.abstractmethod
    def write(self, pcm16: bytes) -> None:
        ...

    def available(self) -> bool:
        return True


class NullAudioDevice(AudioDevice):
    """No real device. Reads silence, discards writes. For dev/tests."""

    def __init__(self, sample_rate: int = 16000) -> None:
        self.sample_rate = sample_rate
        self.written = 0

    def available(self) -> bool:
        return False

    def read(self, n_frames: int) -> bytes:
        return b"\x00\x00" * max(0, n_frames)

    def write(self, pcm16: bytes) -> None:
        self.written += len(pcm16)
