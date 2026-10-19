"""Fault codes and a fault log."""

from __future__ import annotations

import enum
import time
from dataclasses import dataclass, field
from typing import List


class FaultCode(enum.Enum):
    NONE = "NONE"
    ESTOP_ENGAGED = "ESTOP_ENGAGED"
    WATCHDOG_TIMEOUT = "WATCHDOG_TIMEOUT"
    COMM_LOST = "COMM_LOST"
    JOINT_OUT_OF_RANGE = "JOINT_OUT_OF_RANGE"
    OVER_VELOCITY = "OVER_VELOCITY"
    OVER_TEMPERATURE = "OVER_TEMPERATURE"
    SENSOR_FAULT = "SENSOR_FAULT"
    AI_PROVIDER_FAILURE = "AI_PROVIDER_FAILURE"
    CONFIG_INVALID = "CONFIG_INVALID"
    UNKNOWN = "UNKNOWN"


@dataclass
class FaultEvent:
    code: FaultCode
    detail: str
    ts: float = field(default_factory=time.time)


class FaultLog:
    def __init__(self, max_events: int = 1000) -> None:
        self._events: List[FaultEvent] = []
        self._max = max_events

    def record(self, code: FaultCode, detail: str = "") -> FaultEvent:
        evt = FaultEvent(code=code, detail=detail)
        self._events.append(evt)
        if len(self._events) > self._max:
            self._events = self._events[-self._max :]
        return evt

    @property
    def active(self) -> bool:
        return any(e.code is not FaultCode.NONE for e in self._events[-1:])

    def events(self) -> List[FaultEvent]:
        return list(self._events)

    def latest(self) -> FaultEvent:
        return self._events[-1] if self._events else FaultEvent(FaultCode.NONE, "")
