"""Data models for motion requests and per-joint commands.

These models are deliberately strict. Any field that is missing, out of
range, non-finite or malformed raises :class:`MotionValidationError` so
that malformed input (including anything produced by an AI provider)
cannot reach a motor driver.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional


class MotionValidationError(ValueError):
    """Raised when a motion request fails validation."""


def _check_finite(name: str, value: object) -> float:
    try:
        v = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise MotionValidationError(f"{name} is not a number: {value!r}") from exc
    if math.isnan(v) or math.isinf(v):
        raise MotionValidationError(f"{name} must be finite, got {v!r}")
    return v


@dataclass(frozen=True)
class JointCommand:
    """A single joint position command.

    position_deg: target joint angle in degrees.
    max_velocity_dps: optional velocity bound in degrees/second (> 0).
    """

    joint: str
    position_deg: float
    max_velocity_dps: Optional[float] = None

    def __post_init__(self) -> None:
        if not isinstance(self.joint, str) or not self.joint.strip():
            raise MotionValidationError(f"joint name must be a non-empty string, got {self.joint!r}")
        object.__setattr__(self, "position_deg", _check_finite(f"{self.joint}.position_deg", self.position_deg))
        if self.max_velocity_dps is not None:
            v = _check_finite(f"{self.joint}.max_velocity_dps", self.max_velocity_dps)
            if v <= 0:
                raise MotionValidationError(f"{self.joint}.max_velocity_dps must be > 0, got {v}")
            object.__setattr__(self, "max_velocity_dps", v)


@dataclass
class MotionRequest:
    """A high-level, bounded motion request.

    A request is a *set* of joint commands that should be applied together,
    plus metadata used for safety bookkeeping.
    """

    commands: List[JointCommand]
    source: str = "unknown"
    priority: int = 0
    deadline_s: Optional[float] = None
    created_at: float = field(default_factory=time.monotonic)
    reason: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.commands, Iterable):
            raise MotionValidationError("commands must be an iterable of JointCommand")
        cmds = list(self.commands)
        if not cmds:
            raise MotionValidationError("motion request must contain at least one joint command")
        normalized: List[JointCommand] = []
        seen = set()
        for c in cmds:
            if not isinstance(c, JointCommand):
                raise MotionValidationError(f"each command must be a JointCommand, got {type(c).__name__}")
            if c.joint in seen:
                raise MotionValidationError(f"duplicate joint in request: {c.joint}")
            seen.add(c.joint)
            normalized.append(c)
        self.commands = normalized
        if not isinstance(self.priority, int):
            raise MotionValidationError("priority must be an int")
        if self.deadline_s is not None:
            d = _check_finite("deadline_s", self.deadline_s)
            if d <= 0:
                raise MotionValidationError(f"deadline_s must be > 0, got {d}")
            self.deadline_s = d

    def joints(self) -> List[str]:
        return [c.joint for c in self.commands]

    def as_dict(self) -> Dict[str, object]:
        return {
            "source": self.source,
            "priority": self.priority,
            "reason": self.reason,
            "commands": [
                {
                    "joint": c.joint,
                    "position_deg": c.position_deg,
                    "max_velocity_dps": c.max_velocity_dps,
                }
                for c in self.commands
            ],
        }
