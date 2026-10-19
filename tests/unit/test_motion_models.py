import math

import pytest

from software.motion_planner.models import (
    JointCommand,
    MotionRequest,
    MotionValidationError,
)


def test_valid_joint_command():
    c = JointCommand("neck_yaw", 10.0, max_velocity_dps=30.0)
    assert c.joint == "neck_yaw"
    assert c.position_deg == 10.0


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_non_finite_position_rejected(bad):
    with pytest.raises(MotionValidationError):
        JointCommand("neck_yaw", bad)


def test_empty_joint_name_rejected():
    with pytest.raises(MotionValidationError):
        JointCommand("  ", 0.0)


def test_non_numeric_position_rejected():
    with pytest.raises(MotionValidationError):
        JointCommand("neck_yaw", "left")


def test_zero_or_negative_velocity_rejected():
    with pytest.raises(MotionValidationError):
        JointCommand("neck_yaw", 0.0, max_velocity_dps=0.0)
    with pytest.raises(MotionValidationError):
        JointCommand("neck_yaw", 0.0, max_velocity_dps=-5.0)


def test_empty_request_rejected():
    with pytest.raises(MotionValidationError):
        MotionRequest(commands=[])


def test_duplicate_joint_rejected():
    with pytest.raises(MotionValidationError):
        MotionRequest(commands=[JointCommand("a", 1.0), JointCommand("a", 2.0)])


def test_non_jointcommand_rejected():
    with pytest.raises(MotionValidationError):
        MotionRequest(commands=[{"joint": "a"}])


def test_bad_deadline_rejected():
    with pytest.raises(MotionValidationError):
        MotionRequest(commands=[JointCommand("a", 1.0)], deadline_s=-1)


def test_as_dict_roundtrip_fields():
    r = MotionRequest(commands=[JointCommand("a", 1.0)], source="test", reason="wave")
    d = r.as_dict()
    assert d["source"] == "test"
    assert d["commands"][0]["joint"] == "a"
