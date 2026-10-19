import json

import pytest

from software.motion_planner.limits import JointLimit, load_joint_limits
from software.motion_planner.models import MotionValidationError


def test_joint_limit_contains_and_clamp():
    lim = JointLimit("neck_yaw", -45, 45, 60)
    assert lim.contains(0)
    assert not lim.contains(90)
    assert lim.clamp(90) == 45
    assert lim.clamp(-90) == -45


def test_bad_limit_min_ge_max():
    with pytest.raises(MotionValidationError):
        JointLimit("x", 10, 10, 5)


def test_bad_limit_velocity():
    with pytest.raises(MotionValidationError):
        JointLimit("x", -1, 1, 0)


def test_load_json_limits(tmp_path):
    p = tmp_path / "limits.json"
    p.write_text(json.dumps({
        "joints": {
            "neck_yaw": {"min_deg": -45, "max_deg": 45, "max_velocity_dps": 60, "verified": False},
            "neck_pitch": {"min_deg": -30, "max_deg": 30, "max_velocity_dps": 60, "verified": True},
        }
    }))
    s = load_joint_limits(str(p))
    assert "neck_yaw" in s
    assert not s.all_verified  # neck_yaw unverified
    assert s.get("neck_pitch").verified


def test_load_missing_field(tmp_path):
    p = tmp_path / "limits.json"
    p.write_text(json.dumps({"joints": {"a": {"min_deg": -1, "max_deg": 1}}}))
    with pytest.raises(MotionValidationError):
        load_joint_limits(str(p))


def test_load_empty_joints(tmp_path):
    p = tmp_path / "limits.json"
    p.write_text(json.dumps({"joints": {}}))
    with pytest.raises(MotionValidationError):
        load_joint_limits(str(p))


def test_load_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_joint_limits("/nonexistent/limits.json")
