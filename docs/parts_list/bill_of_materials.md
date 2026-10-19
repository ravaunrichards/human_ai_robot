# Bill of Materials (Preliminary / Provisional)

**STATUS: PROVISIONAL.** No prices, product links, certifications or
availability are invented. Costs are marked `unknown`. Most parts are
`candidate` or `not_yet_selected`. This is a sensible preliminary configuration
to unblock planning, not a validated purchase list. The machine-readable copy is
`bill_of_materials.csv`.

## Selection status legend
- **confirmed** — part chosen and verified against datasheet (none yet).
- **candidate** — a reasonable preliminary option identified.
- **not_yet_selected** — needs engineering input before choosing.

## Summary by category
| Category | Items | Dominant open risk |
|----------|-------|--------------------|
| Frame | extrusion/brackets/bearings/fasteners | mass vs stiffness vs torque |
| Actuators | neck, eyes/jaw, shoulder, elbow, wrist, hip, knee, ankle, hand | **torque not validated**; sizing method only |
| Sensors | encoders, IMU, temp, current, foot F/T | absolute encoders for safe power-up |
| Controllers | safety MCU, motion MCU, joint drivers | safety MCU must be independent |
| Compute | host SBC/mini-PC | on-device AI for privacy |
| Power | PSU, battery+BMS, contactor | battery safety unvalidated |
| Safety | E-STOP, fuses, PPE | **E-STOP mandatory, independent** |
| Electrical/Cable | connectors, fuses, cable | ratings from datasheets |
| Audio/Vision | mic array, speaker+amp, camera | privacy controls |
| Exterior | silicone face, body panels | realistic skin is R&D |

## Key honest caveats
1. **Actuator torques are not validated.** The CSV lists `torque TBD`; use the
   sizing method in `docs/mechanical_design/mechanical_design.md` with real CAD
   mass properties, then update status to `confirmed`.
2. **No prices or links** are provided because they cannot be verified here;
   fill them in at purchase time with real quotes.
3. **Battery and face-skin systems are deferred** (`not_yet_selected`) because
   they carry the highest safety / R&D risk.
4. The **E-STOP, contactor and fuses are mandatory** and must be sized to the
   finally selected actuator bus.

## How to progress the BOM
- Freeze the DOF list → compute per-joint loads → size actuators → pick drivers
  → derive bus voltage/current → size fuses/cable/contactor → fill wiring
  tables → flip statuses to `confirmed` with datasheet references.
