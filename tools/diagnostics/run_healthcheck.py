#!/usr/bin/env python3
"""Run the simulation health check and print a structured report.

Usage:
    python tools/diagnostics/run_healthcheck.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from software.app import build_stack  # noqa: E402


def main():
    stack = build_stack()
    report = stack["health"].run()
    print("healthy:", report.healthy)
    for name, ok in report.checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} {report.details.get(name,'')}")
    # confirm the safety default
    planner = stack["planner"]
    if planner is not None:
        print("motion_enabled (expected False):", planner.motion_enabled)
    return 0 if report.healthy else 1


if __name__ == "__main__":
    sys.exit(main())
