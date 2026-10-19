"""Camera interfaces and a modular perception layer.

Privacy-first: perception is OFF by default, face recognition is NOT
implemented (only optional face *detection* behind an explicit flag), and
no images are persisted unless a caller explicitly opts in. See
docs/safety/privacy.md.
"""

from .camera import Camera, NullCamera, Frame
from .perception import PerceptionLayer, Detection, PerceptionConfig

__all__ = [
    "Camera",
    "NullCamera",
    "Frame",
    "PerceptionLayer",
    "Detection",
    "PerceptionConfig",
]
