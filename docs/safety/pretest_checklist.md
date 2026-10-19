# Pre-Test Checklist (run before EVERY powered test)

All items must be checked by a qualified operator. If any item fails, STOP.

## Environment
- [ ] Keep-out zone established; only trained personnel inside.
- [ ] Robot externally supported (gantry/stand) — not free-standing.
- [ ] Clear escape path; nothing fragile/valuable in reach.
- [ ] Fire extinguisher + first-aid available; emergency numbers posted.

## E-STOP & power
- [ ] Manual E-STOP tested to physically remove actuator-bus power (verified
      with meter, de-energised then at low voltage).
- [ ] Power isolation/disconnect accessible and operational.
- [ ] Fuses correct rating; no visible wiring damage.
- [ ] Logic and actuator domains correct; grounds verified.

## Software / config
- [ ] `simulation_only` set correctly for the intended test.
- [ ] Joint limits loaded and, for enabling motion, every joint `verified`.
- [ ] `python -m pytest tests/safety -q` passes on the deployed code.
- [ ] Watchdog timeouts configured; heartbeat verified in sim first.
- [ ] Motion speeds set to commissioning-low values.

## Mechanical
- [ ] Mechanical stops present; covers over pinch points and head mechanism.
- [ ] Fasteners torqued; no loose cabling in motion path.

## Sign-off
- [ ] Operator: ____________  Date/Time: ____________
- [ ] Safety reviewer: ____________  (required for load-bearing/human-proximate)
