"""Modular perception layer.

Perception is a pluggable pipeline of detectors. No detector is bundled;
the default pipeline is empty, which means the layer reports 'no
perception backend installed'. This keeps the project honest: person /
object detection requires models that are not shipped here.

Privacy controls:
  * enabled=False by default.
  * allow_face_detection=False by default; face RECOGNITION is never
    implemented in this repository.
  * persist_frames=False by default; frames are never written to disk
    unless explicitly enabled by the operator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List

from .camera import Frame


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: tuple  # (x, y, w, h) in pixels


@dataclass
class PerceptionConfig:
    enabled: bool = False
    allow_face_detection: bool = False
    persist_frames: bool = False


Detector = Callable[[Frame], List[Detection]]


class PerceptionLayer:
    def __init__(self, config: PerceptionConfig = None, detectors: List[Detector] = None) -> None:
        self.config = config or PerceptionConfig()
        self._detectors: List[Detector] = list(detectors or [])

    def add_detector(self, detector: Detector) -> None:
        self._detectors.append(detector)

    def backend_installed(self) -> bool:
        return bool(self._detectors)

    def process(self, frame: Frame) -> List[Detection]:
        if not self.config.enabled:
            return []
        if not self._detectors:
            # Honest limitation: no model installed.
            return []
        out: List[Detection] = []
        for det in self._detectors:
            out.extend(det(frame))
        return out

    def describe_scene(self, frame: Frame) -> str:
        dets = self.process(frame)
        if not self.config.enabled:
            return "perception disabled"
        if not self._detectors:
            return "no perception backend installed"
        if not dets:
            return "no objects detected"
        labels = {}
        for d in dets:
            labels[d.label] = labels.get(d.label, 0) + 1
        return ", ".join(f"{n} {label}" for label, n in sorted(labels.items()))
