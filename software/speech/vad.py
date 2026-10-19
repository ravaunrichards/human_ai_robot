"""Voice activity detection.

A dependency-free energy-based VAD is provided as a baseline. Real
deployments can replace it with WebRTC VAD or Silero VAD via subclass.
"""

from __future__ import annotations

import abc
import struct


class VoiceActivityDetector(abc.ABC):
    @abc.abstractmethod
    def is_speech(self, pcm16: bytes, sample_rate: int = 16000) -> bool:
        ...


class EnergyVAD(VoiceActivityDetector):
    def __init__(self, threshold_rms: float = 500.0) -> None:
        self._threshold = threshold_rms

    def rms(self, pcm16: bytes) -> float:
        if len(pcm16) < 2:
            return 0.0
        n = len(pcm16) // 2
        samples = struct.unpack("<" + "h" * n, pcm16[: n * 2])
        if not samples:
            return 0.0
        acc = sum(s * s for s in samples)
        return (acc / n) ** 0.5

    def is_speech(self, pcm16: bytes, sample_rate: int = 16000) -> bool:
        return self.rms(pcm16) >= self._threshold
