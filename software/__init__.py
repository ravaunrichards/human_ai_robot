"""human_ai_robot software package.

Top-level package for the AI-computer side software of the human-sized
female humanoid robot project. Subpackages are intentionally modular so
that real hardware drivers, AI providers and speech/vision backends can
be swapped in later without touching safety-critical logic.

SAFETY NOTE: nothing in this package enables real actuator outputs. The
default hardware interface is a simulation. See docs/safety/.
"""

__version__ = "0.1.0"
__status__ = "pre-alpha / simulation-only"
