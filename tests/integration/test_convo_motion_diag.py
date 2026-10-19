"""Integration: conversation -> bounded intention -> motion planner -> diag.

Demonstrates that an AI reply cannot directly move hardware; a separate,
validated motion request is required, and remains undispatched unless the
safety gate is satisfied.
"""

from software.conversation import ConversationManager, EchoProvider
from software.diagnostics import FaultCode, FaultLog, HealthMonitor
from software.hardware_interfaces import SimulatedHardware
from software.motion_planner import JointCommand, MotionPlanner, MotionRequest
from software.motion_planner.limits import JointLimit, JointLimitSet


def _limits():
    return JointLimitSet(
        {"neck_yaw": JointLimit("neck_yaw", -45, 45, 60, verified=True)},
        all_verified=True,
    )


def test_ai_reply_does_not_move_hardware():
    hw = SimulatedHardware()
    planner = MotionPlanner(_limits(), hw)
    convo = ConversationManager([EchoProvider()])
    reply = convo.reply("turn your head")
    assert isinstance(reply, str)
    # The AI reply is text only; hardware untouched.
    assert hw.read_state().positions_deg == {}


def test_bounded_intention_flows_through_planner():
    hw = SimulatedHardware()
    planner = MotionPlanner(_limits(), hw)
    faults = FaultLog()
    # A behaviour layer (not the LLM) produces a bounded request.
    req = MotionRequest([JointCommand("neck_yaw", 15.0)], source="behaviour")
    dispatched, result = planner.submit(req)
    assert result.ok is True
    assert dispatched is False  # gate still closed
    if not dispatched:
        faults.record(FaultCode.NONE, "request validated, motion gate closed")
    assert faults.latest().code is FaultCode.NONE


def test_health_reflects_estop():
    hw = SimulatedHardware()
    hm = HealthMonitor()
    hm.register("estop_clear", lambda: (not hw.read_state().estop_active, ""))
    assert hm.run().healthy
    hw.estop()
    assert not hm.run().healthy
