#!/usr/bin/env bash
# Run the full test suite from the repo root.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
python -m pytest -q "$@"
