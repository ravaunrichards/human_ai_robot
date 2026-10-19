import pytest

from software.hardware_interfaces import SimulatedHardware


class FakeClock:
    def __init__(self):
        self.t = 0.0
    def __call__(self):
        return self.t


def test_commands_rejected_when_disabled():
    hw = SimulatedHardware()
    with pytest.raises(RuntimeError):
        hw.send_joint_commands([("a", 1.0, 10.0)])


def test_enable_then_command():
    hw = SimulatedHardware()
    hw.enable()
    hw.send_joint_commands([("a", 1.0, 10.0)])
    assert hw.read_state().positions_deg["a"] == 1.0


def test_estop_blocks_and_disables():
    hw = SimulatedHardware()
    hw.enable()
    hw.estop()
    assert hw.read_state().estop_active
    with pytest.raises(RuntimeError):
        hw.send_joint_commands([("a", 1.0, 10.0)])
    with pytest.raises(RuntimeError):
        hw.enable()  # cannot enable during estop


def test_clear_estop_allows_reenable():
    hw = SimulatedHardware()
    hw.estop()
    hw.clear_estop()
    hw.enable()
    assert hw.read_state().enabled


def test_watchdog_expiry_disables():
    clk = FakeClock()
    hw = SimulatedHardware(watchdog_timeout_s=0.5, clock=clk)
    hw.enable()
    hw.feed_heartbeat()
    clk.t = 1.0  # advance beyond timeout
    hw.tick()
    state = hw.read_state()
    assert state.enabled is False
    assert "WATCHDOG_TIMEOUT" in state.fault_codes
