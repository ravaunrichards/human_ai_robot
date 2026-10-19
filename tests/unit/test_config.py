import json

import pytest

from software.configuration import ConfigError, load_config


def test_defaults_simulation_only():
    cfg = load_config(environ={})
    assert cfg.simulation_only is True
    assert cfg.motion_enabled_default is False


def test_env_override_bool():
    cfg = load_config(environ={"ROBOT_SPEECH_ENABLED": "true"})
    assert cfg.speech_enabled is True


def test_api_keys_from_env_only():
    cfg = load_config(environ={"OPENAI_API_KEY": "secret", "OTHER": "x"})
    assert cfg.api_keys == {"OPENAI_API_KEY": "secret"}


def test_invalid_motion_default_rejected():
    with pytest.raises(ConfigError):
        load_config(environ={
            "ROBOT_SIMULATION_ONLY": "false",
            "ROBOT_MOTION_ENABLED_DEFAULT": "true",
        })


def test_unknown_provider_rejected():
    with pytest.raises(ConfigError):
        load_config(environ={"ROBOT_CONVERSATION_PROVIDER": "magic"})


def test_load_from_file(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"speech_enabled": True, "vision_enabled": True}))
    cfg = load_config(str(p), environ={})
    assert cfg.speech_enabled and cfg.vision_enabled
