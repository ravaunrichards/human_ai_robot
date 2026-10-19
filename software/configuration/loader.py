"""Application configuration loader.

Loads layered configuration from a YAML/JSON file plus environment
variables. API keys are read ONLY from the environment and are never
stored in the config file or logged. See .env.example.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class ConfigError(ValueError):
    pass


@dataclass
class AppConfig:
    simulation_only: bool = True
    motion_enabled_default: bool = False
    joint_limits_path: str = "configuration/joint_limits/preliminary_limits.json"
    conversation_provider: str = "local"
    online_ai_enabled: bool = False
    speech_enabled: bool = False
    vision_enabled: bool = False
    log_level: str = "INFO"
    raw: Dict[str, Any] = field(default_factory=dict)
    # API keys are populated from env only, never from file.
    api_keys: Dict[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.simulation_only and self.motion_enabled_default:
            raise ConfigError(
                "refusing config: motion_enabled_default must be False unless "
                "explicitly commissioned on real hardware"
            )
        if self.conversation_provider not in ("local", "online", "echo"):
            raise ConfigError(f"unknown conversation_provider: {self.conversation_provider}")


def _read_file(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml  # type: ignore

            data = yaml.safe_load(text) or {}
        except ImportError as exc:
            raise ConfigError("PyYAML required for YAML config") from exc
    else:
        data = json.loads(text) if text.strip() else {}
    if not isinstance(data, dict):
        raise ConfigError("config file must deserialize to a mapping")
    return data


def _collect_api_keys(environ: Dict[str, str]) -> Dict[str, str]:
    keys = {}
    for name, value in environ.items():
        if name.endswith("_API_KEY") and value:
            keys[name] = value
    return keys


def load_config(path: Optional[str] = None, environ: Optional[Dict[str, str]] = None) -> AppConfig:
    environ = dict(os.environ if environ is None else environ)
    data = _read_file(path) if path else {}

    def pick(key: str, default: Any) -> Any:
        env_key = "ROBOT_" + key.upper()
        if env_key in environ:
            val = environ[env_key]
            if isinstance(default, bool):
                return val.strip().lower() in ("1", "true", "yes", "on")
            return val
        return data.get(key, default)

    cfg = AppConfig(
        simulation_only=bool(pick("simulation_only", True)),
        motion_enabled_default=bool(pick("motion_enabled_default", False)),
        joint_limits_path=str(pick("joint_limits_path", AppConfig.joint_limits_path)),
        conversation_provider=str(pick("conversation_provider", "local")),
        online_ai_enabled=bool(pick("online_ai_enabled", False)),
        speech_enabled=bool(pick("speech_enabled", False)),
        vision_enabled=bool(pick("vision_enabled", False)),
        log_level=str(pick("log_level", "INFO")),
        raw=data,
        api_keys=_collect_api_keys(environ),
    )
    cfg.validate()
    return cfg
