#!/usr/bin/env python3
"""Reproducible parametric skeleton LAYOUT (not a manufacturing model).

Generates a schematic point/segment skeleton for a ~1.65 m standing figure and
writes joint-frame coordinates to JSON. Dimensions are PRELIMINARY targets.

Usage:
    python hardware/cad/skeleton_layout.py --out hardware/cad/skeleton.json
"""
from __future__ import annotations

import argparse
import json

# Preliminary proportion targets (metres), origin at floor between feet.
HEIGHT = 1.65
P = {
    "height_m": HEIGHT,
    "shoulder_width_m": 0.37,
    "hip_width_m": 0.30,
    "status": "PRELIMINARY_UNVERIFIED",
}


def build_skeleton():
    sw = P["shoulder_width_m"] / 2
    hw = P["hip_width_m"] / 2
    # (x lateral, y forward, z up). Heights as fractions of total height.
    joints = {
        "floor": (0.0, 0.0, 0.00),
        "pelvis": (0.0, 0.0, 0.53 * HEIGHT),
        "hip_l": (-hw, 0.0, 0.53 * HEIGHT),
        "hip_r": (hw, 0.0, 0.53 * HEIGHT),
        "knee_l": (-hw, 0.0, 0.28 * HEIGHT),
        "knee_r": (hw, 0.0, 0.28 * HEIGHT),
        "ankle_l": (-hw, 0.0, 0.04 * HEIGHT),
        "ankle_r": (hw, 0.0, 0.04 * HEIGHT),
        "waist": (0.0, 0.0, 0.62 * HEIGHT),
        "chest": (0.0, 0.0, 0.80 * HEIGHT),
        "shoulder_l": (-sw, 0.0, 0.82 * HEIGHT),
        "shoulder_r": (sw, 0.0, 0.82 * HEIGHT),
        "elbow_l": (-sw, 0.0, 0.63 * HEIGHT),
        "elbow_r": (sw, 0.0, 0.63 * HEIGHT),
        "wrist_l": (-sw, 0.0, 0.46 * HEIGHT),
        "wrist_r": (sw, 0.0, 0.46 * HEIGHT),
        "neck": (0.0, 0.0, 0.86 * HEIGHT),
        "head": (0.0, 0.0, 0.93 * HEIGHT),
    }
    bones = [
        ("floor", "ankle_l"), ("floor", "ankle_r"),
        ("ankle_l", "knee_l"), ("knee_l", "hip_l"),
        ("ankle_r", "knee_r"), ("knee_r", "hip_r"),
        ("hip_l", "pelvis"), ("hip_r", "pelvis"),
        ("pelvis", "waist"), ("waist", "chest"),
        ("chest", "shoulder_l"), ("chest", "shoulder_r"),
        ("shoulder_l", "elbow_l"), ("elbow_l", "wrist_l"),
        ("shoulder_r", "elbow_r"), ("elbow_r", "wrist_r"),
        ("chest", "neck"), ("neck", "head"),
    ]
    return {"params": P, "joints": joints, "bones": bones}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="hardware/cad/skeleton.json")
    args = ap.parse_args()
    model = build_skeleton()
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(model, fh, indent=2)
    print(f"wrote {args.out} with {len(model['joints'])} joints, {len(model['bones'])} bones")
    print("STATUS: PRELIMINARY layout aid — NOT a manufacturing model.")


if __name__ == "__main__":
    main()
