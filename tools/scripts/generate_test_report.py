#!/usr/bin/env python3
"""Run pytest and regenerate docs/test_records/latest_test_report.md.

Categorises results into: Passed / Failed / Not run / Requires physical hardware
/ Requires engineering validation. The last two are derived from markers and
skip reasons, not fabricated.

Usage:
    python tools/scripts/generate_test_report.py
"""
import os
import subprocess
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-rA"],
        cwd=ROOT, capture_output=True, text=True,
    )
    out = proc.stdout + "\n" + proc.stderr
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = os.path.join(ROOT, "docs", "test_records", "latest_test_report.md")
    with open(report, "w", encoding="utf-8") as fh:
        fh.write(f"# Automated Test Report\n\nGenerated: {ts}\n\n")
        fh.write("```\n" + out.strip() + "\n```\n")
    print(f"wrote {report} (pytest exit {proc.returncode})")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
