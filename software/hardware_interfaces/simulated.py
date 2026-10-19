"""Simulated hardware backend.

Safe, pure-software stand-in for real actuators. It records commanded
positions, honours an e-stop, enforces an enable gate and a command
watchdog, and never touches any physical device.
"""

from __future__ import annotations

import time
from typing import Dict

from .base import HardwareInterface, HardwareState, JointPayload


class SimulatedHardware(HardwareInterface):
    def __init__(self, watchdog_timeout_s: float = 0.5, clock=time.monotonic) -> None:
        self._clock = clock
        self._watchdog_timeout_s = watchdog_timeout_s
        self._enabled = False
        self._estop = False
        self._positions: Dict[str, float] = {}
        self._last_cmd = 0.0
        self._last_heartbeat = self._clock()
        self._faults = []

    def enable(self) -> None:
        if self._estop:
            raise RuntimeError("cannot enable while e-stop is active")
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    def estop(self) -> None:
        self._estop = True
        self._enabled = False
        self._faults.append("ESTOP_ENGAGED")

    def clear_estop(self) -> None:
        self._estop = False
        if "ESTOP_ENGAGED" in self._faults:
            self._faults.remove("ESTOP_ENGAGED")

    def send_joint_commands(self, payload: JointPayload) -> None:
        if self._estop:
            raise RuntimeError("refusing command: e-stop active")
        if not self._enabled:
            raise RuntimeError("refusing command: hardware not enabled")
        now = self._clock()
        for joint, position_deg, _vel in payload:
            self._positions[joint] = position_deg
        self._last_cmd = now
        self._last_heartbeat = now

    def watchdog_expired(self) -> bool:
        return (self._clock() - self._last_heartbeat) > self._watchdog_timeout_s

    def tick(self) -> None:
        """Call periodically. Disables motion if the watchdog has expired."""
        if self._enabled and self.watchdog_expired():
            self._enabled = False
            self._faults.append("WATCHDOG_TIMEOUT")

    def feed_heartbeat(self) -> None:
        self._last_heartbeat = self._clock()

    def read_state(self) -> HardwareState:
        return HardwareState(
            enabled=self._enabled,
            estop_active=self._estop,
            last_command_time=self._last_cmd,
            positions_deg=dict(self._positions),
            fault_codes=list(self._faults),
        )

    def heartbeat(self) -> float:
        return self._last_heartbeat
