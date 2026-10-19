from software.motion_planner.safety_gate import SafetyGate


def test_default_gate_forbids_motion():
    g = SafetyGate()
    assert g.motion_permitted() is False
    reasons = g.blocking_reasons()
    assert "simulation_only mode active" in reasons
    assert "joint limits not verified" in reasons


def test_gate_permits_only_when_everything_satisfied():
    g = SafetyGate(
        estop_clear=True,
        limits_verified=True,
        operator_ack=True,
        watchdog_ok=True,
        simulation_only=False,
    )
    assert g.motion_permitted() is True
    assert g.blocking_reasons() == []


def test_simulation_only_always_blocks():
    g = SafetyGate(
        estop_clear=True,
        limits_verified=True,
        operator_ack=True,
        watchdog_ok=True,
        simulation_only=True,
    )
    assert g.motion_permitted() is False
    assert "simulation_only mode active" in g.blocking_reasons()


def test_estop_blocks_motion():
    g = SafetyGate(
        estop_clear=False,
        limits_verified=True,
        operator_ack=True,
        watchdog_ok=True,
        simulation_only=False,
    )
    assert g.motion_permitted() is False
    assert "estop not cleared" in g.blocking_reasons()
