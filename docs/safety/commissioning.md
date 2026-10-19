# Staged Commissioning Procedure

Each stage is independently gated. Do not advance without the pre-test
checklist and the required sign-off (`signoff_record.md`). Keep speeds low and
the robot externally supported until stability is proven.

## Stage 0 — Simulation only
- Run the full test suite and the simulation. No hardware powered.
- Exit criteria: all software/safety tests pass.

## Stage 1 — Bench electrical bring-up (no motion)
- Power logic domain only; verify MCUs boot, comms (CRC frames) healthy.
- Verify E-STOP drops the (de-energised) actuator contactor.
- Exit criteria: comms stable, E-STOP proven, no faults.

## Stage 2 — Single-joint motion on a fixture
- One joint mounted in a secure fixture, off the body.
- Measure real mechanical stops; set verified joint limits for that joint.
- Enable motion ONLY for that joint; verify limits, watchdog, E-STOP under
  motion at low speed.
- Exit criteria: limits hold, watchdog disables on comms loss, E-STOP cuts
  power under motion.

## Stage 3 — Subsystem (e.g. one arm) on a stand
- Repeat limit verification per joint; test coordinated motion, slow.
- Exit criteria: no limit violation, thermal within bounds.

## Stage 4 — Head/face mechanism
- Eyes/eyelids/jaw bring-up; low force but guard eye/jaw pinch.

## Stage 5 — Hands (functional fingers)
- Grasp force limited; verify no entrapment.

## Stage 6 — Whole-body, supported (no balance)
- Full robot on gantry; coordinated non-locomotion motion.

## Stage 7 — Standing balance (HIGH RISK)
- Only after IMU/foot-sensor integration and professional review.

## Stage 8 — Walking / lifting (HIGHEST RISK)
- Separate program; extensive supervised testing; not in scope of this repo.

At every stage: motion stays disabled by default, limits must be `verified`,
and the independent E-STOP must be proven before energising.
