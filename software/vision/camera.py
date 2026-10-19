"""Camera interface."""

from __future__ import annotations

import abc
import time
from dataclasses import dataclass


@dataclass
class Frame:
    width: int
    height: int
    data: bytes  # raw bytes; format negotiated by driver (e.g. RGB888)
    ts: float


class Camera(abc.ABC):
    @abc.abstractmethod
    def grab(self) -> Frame:
        ...

    def available(self) -> bool:
        return True


class NullCamera(Camera):
    """Returns black frames. No real device accessed. For dev/tests."""

    def __init__(self, width: int = 320, height: int = 240) -> None:
        self.width = width
        self.height = height

    def available(self) -> bool:
        return False

    def grab(self) -> Frame:
        return Frame(self.width, self.height, b"\x00" * (self.width * self.height * 3), time.monotonic())
