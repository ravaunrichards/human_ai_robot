"""Health monitoring and health reports."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass
class HealthReport:
    healthy: bool
    checks: Dict[str, bool]
    details: Dict[str, str] = field(default_factory=dict)
    ts: float = field(default_factory=time.time)

    def failed(self) -> List[str]:
        return [name for name, ok in self.checks.items() if not ok]


class HealthMonitor:
    """Registry of named boolean health checks.

    Each check is a callable returning (ok: bool, detail: str).
    """

    def __init__(self) -> None:
        self._checks: Dict[str, Callable[[], object]] = {}

    def register(self, name: str, check: Callable[[], object]) -> None:
        if name in self._checks:
            raise ValueError(f"duplicate health check: {name}")
        self._checks[name] = check

    def run(self) -> HealthReport:
        results: Dict[str, bool] = {}
        details: Dict[str, str] = {}
        for name, check in self._checks.items():
            try:
                outcome = check()
                if isinstance(outcome, tuple):
                    ok, detail = bool(outcome[0]), str(outcome[1])
                else:
                    ok, detail = bool(outcome), ""
            except Exception as exc:  # noqa: BLE001 - health checks must not raise
                ok, detail = False, f"exception: {exc}"
            results[name] = ok
            if detail:
                details[name] = detail
        return HealthReport(healthy=all(results.values()), checks=results, details=details)
