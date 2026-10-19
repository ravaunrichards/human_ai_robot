# Contributing

Thanks for helping build this project responsibly.

## Ground rules
1. **Never weaken a safety control to make a demo work.** The motion gate,
   e-stop handling, joint-limit validation and `simulation_only` default are
   load-bearing. Changes to `software/motion_planner/` or
   `firmware/safety_controller/` require review by someone with robotics safety
   experience.
2. **No secrets in commits.** Keys come from the environment only.
3. **No real motor-output code in examples.** Add real drivers as separate,
   clearly labelled modules that subclass `HardwareInterface`.
4. **Label unverified data.** Dimensions, torques, pinouts and prices must be
   marked `preliminary`, `candidate`, or `not yet selected` until verified.

## Development setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Style & checks
- `ruff check .` for linting (line length 100).
- `mypy software` for type checks (best-effort; not all backends are typed).
- Add tests for every behaviour change. Safety-relevant code needs a test that
  proves the unsafe path is rejected.

## Commit / PR expectations
- Small, focused commits. Describe what changed and what was tested.
- Do not commit `.env`, measured calibration, logs, or vision captures.
- Flag any change that could allow motion on unverified hardware in the PR
  description; such PRs are blocked by default.

## Directory ownership
- `software/` — AI-computer side (Python).
- `firmware/` — real-time controllers (C / starter stubs).
- `docs/` — engineering documentation; keep status labels honest.
- `hardware/` — mechanical notes + CAD sources.
