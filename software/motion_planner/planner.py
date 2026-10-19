"""Motion planner facade.

The :class:`MotionPlanner` is the single choke point between high-level
intentions (from conversation / behaviour code) and the hardware
interface. It validates every request against the loaded joint limits
and the current safety gate before anything is dispatched.

Design rules enforced here:
  * Motion is DISABLED by default. ``enable_motion()`` must be called
    explicitly, and only succeeds when limits are verified AND the
    operator has acknowledged the safety configuration.
  * Every request is validated: unknown joints, out-of-range targets and
    excessive velocities are rejected.
  * A rejected request never reaches the hardware interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from .limits import JointLimitSet
from .models import MotionRequest, MotionValidationError


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]
    clamped_joints: List[str]


class MotionPlanner:
    def __init__(
        self,
        limits: JointLimitSet,
        hardware=None,
        clamp_out_of_range: bool = False,
    ) -> None:
        self._limits = limits
        self._hardware = hardware
        self._clamp = clamp_out_of_range
        self._motion_enabled = False
        self._operator_ack = False

    # ------------------------------------------------------------------ #
    # Safety gate
    # ------------------------------------------------------------------ #
    @property
    def motion_enabled(self) -> bool:
        return self._motion_enabled

    def acknowledge_safety(self, token: str) -> None:
        """Operator acknowledges they have read the safety configuration.

        The exact token is intentionally explicit to make accidental
        enabling in code or by an AI provider effectively impossible.
        """
        if token != "I_HAVE_VERIFIED_HARDWARE_AND_LIMITS":
            raise MotionValidationError("invalid safety acknowledgement token")
        self._operator_ack = True

    def enable_motion(self) -> None:
        if not self._operator_ack:
            raise MotionValidationError(
                "cannot enable motion: operator has not acknowledged safety configuration"
            )
        if not self._limits.all_verified:
            raise MotionValidationError(
                "cannot enable motion: joint limits are not all marked verified"
            )
        if self._hardware is None:
            raise MotionValidationError("cannot enable motion: no hardware interface attached")
        self._motion_enabled = True

    def disable_motion(self) -> None:
        self._motion_enabled = False
        if self._hardware is not None and hasattr(self._hardware, "disable"):
            self._hardware.disable()

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #
    def validate(self, request: MotionRequest) -> ValidationResult:
        errors: List[str] = []
        clamped: List[str] = []
        if not isinstance(request, MotionRequest):
            return ValidationResult(False, ["request is not a MotionRequest"], [])
        for cmd in request.commands:
            if cmd.joint not in self._limits:
                errors.append(f"unknown joint: {cmd.joint}")
                continue
            lim = self._limits.get(cmd.joint)
            if not lim.contains(cmd.position_deg):
                if self._clamp:
                    clamped.append(cmd.joint)
                else:
                    errors.append(
                        f"{cmd.joint}: position {cmd.position_deg} outside "
                        f"[{lim.min_deg}, {lim.max_deg}]"
                    )
            if cmd.max_velocity_dps is not None and cmd.max_velocity_dps > lim.max_velocity_dps:
                errors.append(
                    f"{cmd.joint}: velocity {cmd.max_velocity_dps} exceeds limit "
                    f"{lim.max_velocity_dps}"
                )
        return ValidationResult(ok=not errors, errors=errors, clamped_joints=clamped)

    # ------------------------------------------------------------------ #
    # Dispatch
    # ------------------------------------------------------------------ #
    def submit(self, request: MotionRequest) -> Tuple[bool, ValidationResult]:
        """Validate and (if motion is enabled) dispatch a motion request.

        Returns (dispatched, validation_result). The request is only sent
        to hardware when validation passes AND motion is enabled.
        """
        result = self.validate(request)
        if not result.ok:
            return False, result
        if not self._motion_enabled:
            # Validated but not dispatched: safe default.
            return False, result
        payload = self._build_payload(request, result)
        self._hardware.send_joint_commands(payload)  # type: ignore[union-attr]
        return True, result

    def _build_payload(self, request: MotionRequest, result: ValidationResult):
        payload = []
        for cmd in request.commands:
            lim = self._limits.get(cmd.joint)
            pos = lim.clamp(cmd.position_deg) if self._clamp else cmd.position_deg
            vel = cmd.max_velocity_dps or lim.max_velocity_dps
            payload.append((cmd.joint, pos, min(vel, lim.max_velocity_dps)))
        return payload
