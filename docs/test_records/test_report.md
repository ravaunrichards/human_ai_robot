# Test Report (Categorised)

Environment: Python 3.12, clean install, **simulation only**. No physical
hardware was present or tested. Command: `python -m pytest -q`.

## Result summary
**73 passed, 3 skipped** (the 3 skipped require physical hardware).
See `latest_test_report.md` for the raw pytest output (auto-generated).

## Passed (73)
- `tests/unit/test_motion_models.py` — motion request/command validation
  (non-finite, non-numeric, empty, duplicate joints, bad deadline, velocity).
- `tests/unit/test_joint_limits.py` — limit loading, clamp/contains, bad files.
- `tests/unit/test_config.py` — config parsing, env overrides, API-key-from-env,
  invalid motion-default and provider rejection.
- `tests/unit/test_diagnostics.py` — fault log, health monitor, structured log.
- `tests/unit/test_protocol.py` — CRC framing encode/decode, corruption/timeout.
- `tests/unit/test_conversation.py` — provider availability, offline fallback.
- `tests/unit/test_speech_vision.py` — offline STT/TTS/VAD, perception privacy
  defaults, "no backend installed" honesty.
- `tests/unit/test_simulated_hardware.py` — enable gate, e-stop, watchdog expiry.
- `tests/safety/test_safety_gate.py` — default forbids motion; all conditions.
- `tests/safety/test_planner_safety.py` — motion disabled by default, cannot
  enable without ack + verified limits, out-of-range/unknown/over-velocity
  rejection, e-stop blocks dispatch, full enable path.
- `tests/integration/test_convo_motion_diag.py` — AI reply does not move
  hardware; bounded intention flows through planner; health reflects e-stop.

## Failed (0)
None.

## Not run (0 beyond skips)
No tests were silently skipped other than the hardware category below.

## Requires physical hardware (3, skipped)
`tests/hardware/test_real_hardware.py` (skipped unless `ROBOT_HARDWARE_PRESENT=1`
AND a commissioned robot is attached):
- e-stop cuts power on real hardware,
- joint range matches mechanical stops,
- watchdog disables actuators on comm loss.
These are documented, supervised, manual bench tests — **not** run here.

## Requires engineering validation (not automatable here)
- Actuator torque/speed/duty-cycle sizing against real mass properties.
- Electrical ratings, fusing, grounding and e-stop wiring vs datasheets.
- Mechanical load paths (FEA), balance/walking dynamics.
- Skin material durability and facial-expression feasibility.

## Honesty statement
No physical hardware testing occurred. No test result was fabricated. The
simulation and safety-logic tests above are the real, reproducible results on a
clean Python environment.
