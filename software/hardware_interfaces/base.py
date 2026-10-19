"""Abstract hardware interface.

Concrete drivers (serial, CAN, EtherCAT, dynamixel, etc.) must subclass
:class:`HardwareInterface`. This repository ships NO such driver; only the
abstract contract and a simulation are provided.
"""

from __future__ import annotations

import abc
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

JointPayload = List[Tuple[str, float, float]]  # (joint, position_deg, velocity_dps)


@dataclass
class HardwareState:
    enabled: bool = False
    estop_active: bool = False
    last_command_time: float = 0.0
    positions_deg: Dict[str, float] = field(default_factory=dict)
    fault_codes: List[str] = field(default_factory=list)


class HardwareInterface(abc.ABC):
    """Contract for any actuator/sensor backend.

    IMPORTANT: implementations must honour ``estop`` and must refuse to
    move while ``estop_active`` is True or ``enabled`` is False.
    """

    @abc.abstractmethod
    def enable(self) -> None:
        ...

    @abc.abstractmethod
    def disable(self) -> None:
        ...

    @abc.abstractmethod
    def estop(self) -> None:
        """Immediately cut actuator motion. Must be independent of software AI."""

    @abc.abstractmethod
    def clear_estop(self) -> None:
        ...

    @abc.abstractmethod
    def send_joint_commands(self, payload: JointPayload) -> None:
        ...

    @abc.abstractmethod
    def read_state(self) -> HardwareState:
        ...

    @abc.abstractmethod
    def heartbeat(self) -> float:
        """Return monotonic timestamp of last successful controller contact."""
