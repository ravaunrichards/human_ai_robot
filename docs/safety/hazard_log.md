# Hazard Log (Living Document)

Append new hazards; never delete. Status: OPEN / MITIGATED / ACCEPTED / CLOSED.

| ID | Date | Hazard | Source | Mitigation ref | Status | Owner |
|----|------|--------|--------|----------------|--------|-------|
| H1 | 2026-10-20 | Limb strike/crush | risk_assessment H1 | E-STOP + gate + support | OPEN | safety eng |
| H2 | 2026-10-20 | Fall onto person | risk_assessment H2 | gantry until balance | OPEN | mech eng |
| H3 | 2026-10-20 | Pinch points | design review | covers + limits | OPEN | mech eng |
| H6 | 2026-10-20 | Software runaway | arch review | MCU revalidation + watchdog | OPEN | emb eng |
| H9 | 2026-10-20 | Power-up motion | arch review | disabled-by-default + abs encoders | OPEN | emb eng |

## Notes
- All entries are OPEN because no hardware exists yet and no mitigation has been
  verified on a physical build. Do not mark MITIGATED without test evidence in
  `docs/test_records/`.
