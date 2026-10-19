#!/usr/bin/env python3
"""Centre-of-mass estimator skeleton.

Reads a simple JSON list of parts [{name, mass_kg, pos_m:[x,y,z]}] and prints
the aggregate mass and CoM. Reproducible method for the mass budget. Masses
must come from real part data; placeholder input yields a placeholder result.

Usage:
    python tools/calibration/com_estimator.py parts.json
"""
import json
import sys


def estimate(parts):
    total = sum(p["mass_kg"] for p in parts)
    if total <= 0:
        raise ValueError("total mass must be > 0")
    com = [sum(p["mass_kg"] * p["pos_m"][i] for p in parts) / total for i in range(3)]
    return total, com


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        # demo with placeholder data
        parts = [
            {"name": "torso", "mass_kg": 12.0, "pos_m": [0, 0, 1.0]},
            {"name": "head", "mass_kg": 3.0, "pos_m": [0, 0, 1.5]},
            {"name": "legs", "mass_kg": 20.0, "pos_m": [0, 0, 0.4]},
        ]
        print("(no file given — using PLACEHOLDER demo data)")
    else:
        with open(argv[0], "r", encoding="utf-8") as fh:
            parts = json.load(fh)
    total, com = estimate(parts)
    print(f"total mass = {total:.3f} kg")
    print(f"CoM (x,y,z) = ({com[0]:.3f}, {com[1]:.3f}, {com[2]:.3f}) m")
    print("NOTE: results are only as valid as the input part masses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
