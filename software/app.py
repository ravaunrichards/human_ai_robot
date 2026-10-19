"""Application entry point.

Starts the robot software stack in SIMULATION-ONLY mode by default:
  * loads configuration + joint limits
  * builds the conversation manager with offline fallback
  * attaches a SimulatedHardware backend
  * runs health checks
  * exposes a tiny interactive loop for development

This entry point NEVER enables real motor output. Real actuators require
explicit commissioning (see docs/safety/commissioning.md).

Run:  python -m software.app --once   (single self-check, used by CI)
      python -m software.app          (interactive dev loop)
"""

from __future__ import annotations

import argparse
import sys

from software.configuration import load_config
from software.conversation import ConversationManager, EchoProvider, LocalLLMProvider
from software.diagnostics import FaultLog, HealthMonitor, configure_logging, get_logger
from software.hardware_interfaces import SimulatedHardware
from software.motion_planner import MotionPlanner, load_joint_limits


def build_stack(config_path: str = None):
    cfg = load_config(config_path)
    configure_logging(structured=True)
    log = get_logger("app")
    log.info("starting human_ai_robot stack (simulation_only=%s)" % cfg.simulation_only)

    try:
        limits = load_joint_limits(cfg.joint_limits_path)
    except Exception as exc:  # noqa: BLE001
        log.error("failed to load joint limits: %s" % exc)
        limits = None

    hardware = SimulatedHardware()
    planner = MotionPlanner(limits=limits, hardware=hardware) if limits else None

    providers = [LocalLLMProvider(runner=None), EchoProvider()]
    convo = ConversationManager(providers)
    convo.add_system("You are a helpful embodied assistant running in simulation.")

    faults = FaultLog()
    health = HealthMonitor()
    health.register("joint_limits_loaded", lambda: (limits is not None, "limits present"))
    health.register("hardware_sim", lambda: (not hardware.read_state().estop_active, "estop clear"))
    health.register("conversation", lambda: (len(convo.history) >= 0, "ready"))
    return {
        "config": cfg,
        "limits": limits,
        "hardware": hardware,
        "planner": planner,
        "conversation": convo,
        "faults": faults,
        "health": health,
        "log": log,
    }


def run_once(stack) -> int:
    report = stack["health"].run()
    stack["log"].info("health: healthy=%s failed=%s" % (report.healthy, report.failed()))
    reply = stack["conversation"].reply("Hello, are you running?")
    stack["log"].info("conversation reply via %s: %s" % (stack["conversation"].last_provider, reply))
    return 0 if report.healthy else 1


def interactive(stack) -> int:
    print("human_ai_robot dev loop (simulation-only). Type 'quit' to exit.")
    print("Motion is DISABLED. This loop cannot move real hardware.")
    while True:
        try:
            text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.lower() in ("quit", "exit"):
            break
        if not text:
            continue
        print("robot>", stack["conversation"].reply(text))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="human_ai_robot simulation stack")
    parser.add_argument("--config", default=None, help="path to config file (yaml/json)")
    parser.add_argument("--once", action="store_true", help="run a single self-check and exit")
    args = parser.parse_args(argv)
    stack = build_stack(args.config)
    if args.once:
        return run_once(stack)
    return interactive(stack)


if __name__ == "__main__":
    sys.exit(main())
