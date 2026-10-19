# Risk Assessment (Preliminary)

**Status: PRELIMINARY.** To be reviewed and signed by a qualified safety
engineer before any physical work. Severity S (1 minor – 5 fatal), Likelihood L
(1 rare – 5 frequent), Risk = S x L (before mitigation).

| # | Hazard | S | L | Risk | Mitigation | Residual owner |
|---|--------|---|---|------|-----------|----------------|
| H1 | Limb strike / crush during motion | 5 | 4 | 20 | hardware E-STOP, keep-out zone, low-speed commissioning, external support, software limits+gate | safety eng |
| H2 | Fall of full-size robot onto person | 5 | 3 | 15 | gantry/stand until balance commissioned; no free-standing early | mech eng |
| H3 | Pinch at joints/fingers/jaw | 3 | 4 | 12 | covers, travel limits, pinch-point mitigation in design | mech eng |
| H4 | Electrical shock / short | 4 | 3 | 12 | isolation, fusing, logic/actuator separation, PPE | elec eng |
| H5 | Battery thermal event | 5 | 2 | 10 | BMS, supervised charging, bench PSU first, deferred | elec eng |
| H6 | Runaway due to software fault | 5 | 2 | 10 | MCU re-validates limits, watchdog, E-STOP independent of host | emb eng |
| H7 | AI/network failure causing unsafe action | 4 | 2 | 8 | safety path independent of AI/net; LLM cannot command motors | sw eng |
| H8 | Overheating actuator/driver | 3 | 3 | 9 | temp sensors to safety MCU, duty-cycle limits, cooling | elec/mech |
| H9 | Unexpected power-up motion | 5 | 2 | 10 | motion disabled by default, absolute encoders, enable gate | emb eng |
| H10 | Privacy breach (camera/mic) | 3 | 2 | 6 | perception off by default, no face recognition, no persist | sw eng |

## Method
Identify hazard → estimate S/L → apply mitigations → re-score residual (to be
filled during review) → accept only with sign-off. The highest risks (H1, H2)
mandate external support, keep-out zones and the independent E-STOP for every
powered test.
