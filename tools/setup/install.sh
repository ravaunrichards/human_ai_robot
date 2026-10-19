#!/usr/bin/env bash
# Setup helper for the human_ai_robot software stack (simulation-only).
# Safe: installs Python deps only; touches no hardware.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "[setup] Python version:"
python --version

echo "[setup] creating venv (.venv) ..."
python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[setup] installing core + test extras ..."
pip install --upgrade pip >/dev/null
pip install -e ".[test]"

echo "[setup] running the simulation self-check ..."
python -m software.app --once

echo "[setup] running tests ..."
python -m pytest -q

echo "[setup] done. Activate with: source .venv/bin/activate"
