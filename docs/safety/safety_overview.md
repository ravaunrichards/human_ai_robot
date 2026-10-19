# Safety Overview (MANDATORY READING)

A full-size humanoid robot can **crush, trap, strike or injure** a person. This
project builds safety in from the start and treats it as higher priority than
any feature or demo.

## Core invariants (enforced in software + required in hardware)
1. **Actuator motion is disabled by default.** `MotionPlanner` starts disabled.
2. **Explicit, multi-condition enable.** Real motion needs: operator ack token
   `+` all joint limits `verified` `+` attached hardware `+` NOT simulation-only.
3. **Independent hardware E-STOP** removes actuator-bus power regardless of any
   software or host state. Software safeguards never replace it.
4. **Command validation.** Every motion request is range/velocity checked;
   malformed or out-of-range requests are rejected before dispatch.
5. **Watchdogs & timeouts.** Host heartbeat loss → safe hold → drive disable.
6. **AI cannot command motors.** LLM/network failures or malformed prompts
   cannot bypass limits; the LLM has no path to actuator outputs.
7. **Simulation-only mode** makes real motion impossible.
8. **Example code never enables real motor outputs.**

## Documents in this folder
- `risk_assessment.md` — hazards, likelihood/severity, mitigations.
- `hazard_log.md` — living log of identified hazards + status.
- `emergency_procedure.md` — what to do when something goes wrong.
- `pretest_checklist.md` — run before ANY powered test.
- `commissioning.md` — staged bring-up procedure.
- `signoff_record.md` — required approvals per stage.
- `privacy.md` — camera/microphone/data handling.

## Non-negotiable rules
- No load-bearing or human-proximate operation without supervised testing and
  professional review.
- Walking, standing balance, lifting, finger actuation and facial mechanisms
  are **separate** commissioning stages, each independently gated.
- Never label placeholder joint limits or unverified wiring as “safe”.
