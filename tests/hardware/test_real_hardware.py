"""Tests that REQUIRE physical hardware.

These are skipped automatically unless the environment variable
ROBOT_HARDWARE_PRESENT=1 is set AND a commissioned robot is connected.
They are included to document what must be verified on real hardware; they
MUST NOT be run against an uncommissioned machine.
"""

import os

import pytest

hardware_present = os.environ.get("ROBOT_HARDWARE_PRESENT") == "1"

pytestmark = pytest.mark.skipif(
    not hardware_present,
    reason="requires commissioned physical hardware (ROBOT_HARDWARE_PRESENT=1)",
)


def test_estop_cuts_power_on_real_hardware():
    pytest.skip("manual, supervised test only \u2014 see docs/safety/commissioning.md")


def test_joint_range_matches_mechanical_stops():
    pytest.skip("requires calibration rig \u2014 see docs/calibration/")


def test_watchdog_disables_actuators_on_comm_loss():
    pytest.skip("supervised bench test only")
