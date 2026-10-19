"""Joint limit loading and enforcement.

Joint limits are loaded from configuration (YAML/JSON) and used to clamp
or reject motion commands. Limits shipped with the repository are
PRELIMINARY / PLACEHOLDER values and are explicitly NOT safe for a real
robot until verified against actual hardware. See docs/safety/.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict

from .models import MotionValidationError


@dataclass(frozen=True)
class JointLimit:
    name: str
    min_deg: float
    max_deg: float
    max_velocity_dps: float
    verified: bool = False

    def __post_init__(self) -> None:
        if self.min_deg >= self.max_deg:
            raise MotionValidationError(
                f"joint {self.name}: min_deg ({self.min_deg}) must be < max_deg ({self.max_deg})"
            )
        if self.max_velocity_dps <= 0:
            raise MotionValidationError(
                f"joint {self.name}: max_velocity_dps must be > 0, got {self.max_velocity_dps}"
            )

    def contains(self, position_deg: float) -> bool:
        return self.min_deg <= position_deg <= self.max_deg

    def clamp(self, position_deg: float) -> float:
        return max(self.min_deg, min(self.max_deg, position_deg))


@dataclass
class JointLimitSet:
    limits: Dict[str, JointLimit]
    all_verified: bool = False

    def __contains__(self, joint: str) -> bool:
        return joint in self.limits

    def get(self, joint: str) -> JointLimit:
        if joint not in self.limits:
            raise MotionValidationError(f"no joint limit defined for joint {joint!r}")
        return self.limits[joint]

    def names(self):
        return list(self.limits.keys())


def _coerce_limits(raw: dict) -> JointLimitSet:
    joints = raw.get("joints")
    if not isinstance(joints, dict) or not joints:
        raise MotionValidationError("joint limit file must contain a non-empty 'joints' mapping")
    limits: Dict[str, JointLimit] = {}
    all_verified = True
    for name, spec in joints.items():
        try:
            lim = JointLimit(
                name=name,
                min_deg=float(spec["min_deg"]),
                max_deg=float(spec["max_deg"]),
                max_velocity_dps=float(spec["max_velocity_dps"]),
                verified=bool(spec.get("verified", False)),
            )
        except KeyError as exc:
            raise MotionValidationError(f"joint {name}: missing field {exc}") from exc
        except (TypeError, ValueError) as exc:
            raise MotionValidationError(f"joint {name}: invalid value ({exc})") from exc
        limits[name] = lim
        all_verified = all_verified and lim.verified
    return JointLimitSet(limits=limits, all_verified=all_verified)


def load_joint_limits(path: str) -> JointLimitSet:
    """Load joint limits from a YAML or JSON file.

    YAML is parsed with PyYAML if available; otherwise a .json file is
    required. The function never trusts the file blindly \u2014 every entry is
    validated through :class:`JointLimit`.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"joint limit file not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    raw = None
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml  # type: ignore

            raw = yaml.safe_load(text)
        except ImportError:
            raise MotionValidationError(
                "PyYAML is required to load YAML joint limits; install pyyaml or use JSON"
            )
    else:
        raw = json.loads(text)
    if not isinstance(raw, dict):
        raise MotionValidationError("joint limit file must deserialize to a mapping")
    return _coerce_limits(raw)
