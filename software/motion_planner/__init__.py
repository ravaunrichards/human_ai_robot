"""Motion planning and validation.

This subpackage converts high-level, bounded *intentions* into validated,
range-checked motion requests. A language model or conversation layer is
NEVER allowed to issue raw motor commands directly; everything must pass
through :func:`validate_motion_request`.
"""

from .models import JointCommand, MotionRequest, MotionValidationError
from .limits import JointLimit, JointLimitSet, load_joint_limits
from .planner import MotionPlanner
from .safety_gate import SafetyGate

__all__ = [
    "SafetyGate",
    "JointCommand",
    "MotionRequest",
    "MotionValidationError",
    "JointLimit",
    "JointLimitSet",
    "load_joint_limits",
    "MotionPlanner",
]
