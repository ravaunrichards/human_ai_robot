#!/usr/bin/env python3
"""Validate a joint-limit file and report verification status.

Usage:
    python tools/calibration/validate_limits.py configuration/joint_limits/preliminary_limits.json

Exit code 0 if the file parses and all limits are structurally valid. Prints a
warning (non-fatal) listing joints that are NOT marked verified — those joints
can never be enabled for real motion until measured and verified.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from software.motion_planner.limits import load_joint_limits  # noqa: E402
from software.motion_planner.models import MotionValidationError  # noqa: E402


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("usage: validate_limits.py <limits.json|yaml>")
        return 2
    path = argv[0]
    try:
        s = load_joint_limits(path)
    except (MotionValidationError, FileNotFoundError) as exc:
        print(f"INVALID: {exc}")
        return 1
    print(f"OK: parsed {len(s.names())} joints from {path}")
    unverified = [n for n in s.names() if not s.get(n).verified]
    if unverified:
        print("WARNING: the following joints are NOT verified and cannot be")
        print("         enabled for real motion until measured on hardware:")
        for n in unverified:
            print(f"  - {n}")
    print(f"all_verified = {s.all_verified}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
