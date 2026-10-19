"""Hardware abstraction interfaces.

The real robot will have concrete drivers (serial/CAN/EtherCAT etc.).
This package ships ONLY an abstract base and a simulation. No real motor
output code is included. See docs/safety/.
"""

from .base import HardwareInterface, HardwareState
from .simulated import SimulatedHardware

__all__ = ["HardwareInterface", "HardwareState", "SimulatedHardware"]
