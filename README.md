# human_ai_robot

Engineering + software project for a **realistic, human-sized, female-presenting
humanoid robot** with a physical body. This repository is **simulation-first and
safety-gated**: it contains the organized project needed to progress toward a
physical build, not a manufactured machine.

> **Honest status (read this first).** No hardware has been fabricated, powered,
> or tested. All dimensions, torques, pinouts, prices and joint limits here are
> **preliminary and unverified**. The runnable code targets a **simulated**
> robot only; it cannot and does not drive real motors. A physical build
> requires qualified engineers and the staged commissioning in `docs/safety/`.

## What this project builds
- A modular **AI-computer software stack** (Python): conversation, speech,
  vision, motion planning, diagnostics, hardware abstraction, configuration.
- A **real-time controller firmware** starter layer (motion / joint / sensor /
  safety controllers) with a shared communication protocol.
- **Mechanical, electrical, wiring, BOM, assembly, calibration, maintenance and
  safety documentation**, with explicit status labels.
- A **test suite** that runs today on a clean Python install (simulation only).

## What is implemented vs. still a proposal
| Area | Status |
|------|--------|
| Motion request models + validation | **Implemented**, tested |
| Joint-limit loading + enforcement | **Implemented**, tested (limits are placeholder) |
| Safety gate (motion disabled by default) | **Implemented**, tested |
| Simulated hardware + watchdog + e-stop | **Implemented**, tested |
| Conversation manager + provider fallback | **Implemented**, tested |
| Speech (STT/TTS/VAD/audio) interfaces | **Interfaces + offline no-op**, real engines not bundled |
| Vision camera + perception layer | **Interfaces + privacy defaults**, no model bundled |
| Comm protocol (framing + CRC) | **Implemented**, tested |
| Firmware controllers | **Starter stubs / specs**, not flashed or tested |
| Mechanical CAD | **Parametric script + specs**, not manufactured |
| Electrical wiring tables | **Conceptual**, not matched to final datasheets |
| Real motor drivers | **Not implemented by design** (safety) |

## System architecture (short)
Hybrid: a **local real-time control layer** owns all time-critical and
safety-critical functions (joint limits, watchdogs, fault handling, e-stop) and
never depends on the internet or a language model. A **high-level computer**
runs conversation/speech/vision and produces *bounded intentions*, which are
turned into validated motion requests by the motion planner. The LLM can never
issue raw motor commands. Full detail: `docs/system_architecture/`.

```
[Mic/Cam] -> [Speech/Vision] -> [Conversation + Behaviour] -> bounded intention
                                               |
                                       [Motion Planner] --validate--> reject
                                               | (only if safety gate open)
                                   [Comm protocol: CRC frames]
                                               |
              [Safety MCU]  <->  [Motion MCU]  <->  [Joint modules] (real-time)
                   |  independent E-STOP + power isolation (hardware)
```

## Prerequisites
- **Software/simulation:** Python 3.9+ (tested on 3.12). No third-party packages
  required for the core + tests.
- **Optional backends:** PyYAML (YAML configs), speech/vision/online-ai extras
  (see `pyproject.toml`).
- **Hardware (future):** out of scope to run here; see BOM and electrical docs.

## Install
```bash
cd human_ai_robot
python -m venv .venv && source .venv/bin/activate   # optional
pip install -e ".[test]"        # core + pytest
# or just run with no install — the core has no third-party deps
```

## Run the simulation
```bash
# single self-check (used by CI), prints structured logs and exits 0
python -m software.app --once

# interactive dev loop (text only; cannot move hardware)
python -m software.app
```

## Run the tests
```bash
python -m pytest -q
# subsets:
python -m pytest tests/safety -q
python -m pytest tests/unit tests/integration -q
```
See `docs/test_records/latest_test_report.md` for the recorded results and the
passed / failed / not-run / requires-hardware / requires-engineering-validation
breakdown.

## Configure local and online AI
- Default provider is **local** with an automatic **offline echo** fallback, so
  the robot always has a response path even with no model and no internet.
- Set `ROBOT_CONVERSATION_PROVIDER=local|online|echo`.
- Online AI is optional, behind a replaceable adapter, and `requires_internet`.
- See `docs/system_architecture/ai_architecture.md`.

## Protect API keys
- Copy `.env.example` to `.env` (git-ignored) and set keys there.
- Keys are read **only** from the environment (any `*_API_KEY`), never from
  config files or source, and never logged. See `SECURITY.md`.

## Prepare hardware configuration (when you get there)
1. Measure real mechanical stops on the fabricated frame.
2. Edit `configuration/joint_limits/preliminary_limits.json`, set verified
   values and `"verified": true` **per joint** (only after measurement).
3. Follow the staged commissioning in `docs/safety/commissioning.md`.
4. Only then can `MotionPlanner.enable_motion()` succeed — and only outside
   `simulation_only` mode, with the explicit acknowledgement token.

## Troubleshooting
| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `enable_motion` raises | limits not verified / no ack / sim-only | expected safety behaviour; see above |
| YAML config errors | PyYAML missing | `pip install pyyaml` or use JSON |
| conversation returns `[offline-echo]` | no local/online provider available | install a model or set keys |
| import errors in tests | ran outside repo root | run `pytest` from `human_ai_robot/` |

## Steps that REQUIRE qualified engineering review
Mechanical load paths, actuator sizing, electrical protection and grounding,
battery safety, e-stop wiring, joint-limit verification, and **any** powering or
motion of real hardware. Do not skip `docs/safety/`.

## Staged roadmap
1. Architecture, safety requirements, interfaces (**done in this repo**).
2. Simulation, configuration, diagnostics, tests (**done**).
3. Mechanical layout + preliminary BOM (**docs present, unverified**).
4. Electrical architecture + hardware-selection dependencies (**docs present**).
5. AI/speech/vision/motion interfaces (**done; real backends pending**).
6. Firmware starter + comm docs (**stubs/specs present**).
7. Frame fabrication → subsystem bring-up → staged commissioning (**future, supervised**).
8. Whole-body integration (**future, supervised**).

## Repository layout
See section "Repository structure" in `docs/system_architecture/overview.md`
and the per-directory `README.md` files. Directories without implemented code
contain a status README explaining what is needed next.

## License & safety notice
MIT (see `LICENSE`), plus a safety notice: this project is **not** certified
safe to operate as a physical machine. See `SECURITY.md` and `docs/safety/`.
