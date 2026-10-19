"""Standalone safety-gate helper.

A small, auditable object that models the layered conditions required
before real motion is permitted. Kept separate from the planner so it can
be unit-tested in isolation and reused by firmware-facing tooling.

All conditions default to the SAFE (motion-forbidden) state.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SafetyGate:
    estop_clear: bool = False
    limits_verified: bool = False
    operator_ack: bool = False
    simulation_only: bool = True
    watchdog_ok: bool = False

    def motion_permitted(self) -> bool:
        """Real motion is permitted ONLY when every condition is satisfied
        AND we are not in simulation-only mode."""
        return (
            self.estop_clear
            and self.limits_verified
            and self.operator_ack
            and self.watchdog_ok
            and not self.simulation_only
        )

    def blocking_reasons(self):
        reasons = []
        if not self.estop_clear:
            reasons.append("estop not cleared")
        if not self.limits_verified:
            reasons.append("joint limits not verified")
        if not self.operator_ack:
            reasons.append("operator has not acknowledged safety config")
        if not self.watchdog_ok:
            reasons.append("watchdog not healthy")
        if self.simulation_only:
            reasons.append("simulation_only mode active")
        return reasons
