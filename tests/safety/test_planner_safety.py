import pytest

from software.hardware_interfaces import SimulatedHardware
from software.motion_planner import (
    JointCommand,
    MotionPlanner,
    MotionRequest,
    MotionValidationError,
)
from software.motion_planner.limits import JointLimit, JointLimitSet


def make_limits(verified=True):
    return JointLimitSet(
        limits={
            "neck_yaw": JointLimit("neck_yaw", -45, 45, 60, verified=verified),
            "neck_pitch": JointLimit("neck_pitch", -30, 30, 60, verified=verified),
        },
        all_verified=verified,
    )


def test_motion_disabled_by_default():
    planner = MotionPlanner(make_limits(), SimulatedHardware())
    assert planner.motion_enabled is False


def test_valid_request_not_dispatched_when_disabled():
    hw = SimulatedHardware()
    planner = MotionPlanner(make_limits(), hw)
    req = MotionRequest([JointCommand("neck_yaw", 10.0)], source="test")
    dispatched, result = planner.submit(req)
    assert result.ok is True
    assert dispatched is False  # safe default: validated but not moved
    assert hw.read_state().positions_deg == {}


def test_cannot_enable_without_ack():
    planner = MotionPlanner(make_limits(), SimulatedHardware())
    with pytest.raises(MotionValidationError):
        planner.enable_motion()


def test_cannot_enable_with_unverified_limits():
    planner = MotionPlanner(make_limits(verified=False), SimulatedHardware())
    planner.acknowledge_safety("I_HAVE_VERIFIED_HARDWARE_AND_LIMITS")
    with pytest.raises(MotionValidationError):
        planner.enable_motion()


def test_bad_ack_token_rejected():
    planner = MotionPlanner(make_limits(), SimulatedHardware())
    with pytest.raises(MotionValidationError):
        planner.acknowledge_safety("please")


def test_out_of_range_rejected():
    planner = MotionPlanner(make_limits(), SimulatedHardware())
    req = MotionRequest([JointCommand("neck_yaw", 999.0)])
    dispatched, result = planner.submit(req)
    assert dispatched is False
    assert result.ok is False
    assert any("outside" in e for e in result.errors)


def test_unknown_joint_rejected():
    planner = MotionPlanner(make_limits(), SimulatedHardware())
    req = MotionRequest([JointCommand("left_eyebrow", 1.0)])
    _, result = planner.submit(req)
    assert result.ok is False
    assert any("unknown joint" in e for e in result.errors)


def test_over_velocity_rejected():
    planner = MotionPlanner(make_limits(), SimulatedHardware())
    req = MotionRequest([JointCommand("neck_yaw", 10.0, max_velocity_dps=9999.0)])
    _, result = planner.submit(req)
    assert result.ok is False
    assert any("velocity" in e for e in result.errors)


def test_full_enable_then_dispatch():
    hw = SimulatedHardware()
    planner = MotionPlanner(make_limits(verified=True), hw)
    planner.acknowledge_safety("I_HAVE_VERIFIED_HARDWARE_AND_LIMITS")
    planner.enable_motion()
    hw.enable()
    req = MotionRequest([JointCommand("neck_yaw", 20.0)])
    dispatched, result = planner.submit(req)
    assert dispatched is True
    assert result.ok is True
    assert hw.read_state().positions_deg["neck_yaw"] == 20.0


def test_estop_blocks_dispatch():
    hw = SimulatedHardware()
    planner = MotionPlanner(make_limits(verified=True), hw)
    planner.acknowledge_safety("I_HAVE_VERIFIED_HARDWARE_AND_LIMITS")
    planner.enable_motion()
    hw.enable()
    hw.estop()
    req = MotionRequest([JointCommand("neck_yaw", 20.0)])
    with pytest.raises(RuntimeError):
        planner.submit(req)
