# Degrees of Freedom (Proposed)

**Status: PRELIMINARY.** Ranges are design targets; the shipped placeholder
limits in `configuration/joint_limits/preliminary_limits.json` are a reduced,
UNVERIFIED subset. Real ranges must be measured on the fabricated frame.

| Region | Joint | DOF | Proposed range | Notes |
|--------|-------|-----|----------------|-------|
| Neck | yaw / pitch / roll | 3 | ±60 / ±25 / ±20 | safe travel TBD |
| Eyes | each eye yaw | 2 | ±30 | fast, low torque |
| Eyelids | each lid | 2 | 0–25 | cosmetic + blink |
| Brows | each brow | 2 | small | *where practical*; may be decorative |
| Jaw | open/close | 1 | 0–20 | lip-sync support |
| Shoulder | pitch/roll/yaw | 3x2 | large | highest arm torque |
| Elbow | flex | 1x2 | 0–135 | |
| Wrist | pitch/roll | 2x2 | ±45 | |
| Hand | fingers | varies | varies | **functional vs decorative distinguished below** |
| Hip | pitch/roll/yaw | 3x2 | large | highest leg torque |
| Knee | flex | 1x2 | 0–130 | |
| Ankle | pitch/roll | 2x2 | ±20 | balance-critical |

## Hands: functional vs decorative
Dexterous five-finger actuation is **not assumed achievable** in early builds.
Proposed phasing:
- **Phase A (functional):** thumb + index/middle as a 2–3 DOF driven grasp;
  remaining fingers compliant/decorative with passive springs.
- **Phase B:** add independent finger actuation if tendon routing and actuator
  packaging prove feasible.
Document clearly on the hand assembly which fingers are driven vs decorative.

## Facial mechanisms
Eyes/eyelids/jaw are the baseline. Rich facial *expressions* (cheeks, lips,
brows) depend on skin compliance and many small actuators and are treated as a
separate, unvalidated commissioning stage — see `skin_system.md`.
