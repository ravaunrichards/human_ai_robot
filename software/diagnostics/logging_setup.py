"""Structured logging setup.

Provides JSON-ish structured log records with consistent fields so logs
from the AI computer and simulated hardware can be correlated. Falls back
to plain formatting when a TTY is detected.
"""

from __future__ import annotations

import json
import logging
import sys
import time

_CONFIGURED = False


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": round(time.time(), 3),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for key in ("joint", "fault_code", "component", "request_source"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: int = logging.INFO, structured: bool = True) -> None:
    global _CONFIGURED
    handler = logging.StreamHandler(sys.stderr)
    if structured:
        handler.setFormatter(StructuredFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root = logging.getLogger("human_ai_robot")
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
    root.propagate = False
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    if not _CONFIGURED:
        configure_logging()
    return logging.getLogger(f"human_ai_robot.{name}")
