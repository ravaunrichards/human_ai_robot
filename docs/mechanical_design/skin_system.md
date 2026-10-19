# Facial Shell & Skin System (Proposed, High-Risk)

**Status: CONCEPTUAL — UNVALIDATED.** Realistic human-like skin and facial
expression are **not** assumed achievable. This document records the approach,
challenges and dependencies honestly.

## Approach
- Rigid sub-structure (printed/machined) carries a **replaceable** elastomer
  face shell.
- Candidate skin materials: platinum-cure silicone (e.g. Shore 00-20 to 10A
  ranges) with flocking/painting for appearance. **Material selection is not
  finalised and is not validated for durability or safety.**
- Attachment: perimeter capture ring + magnetic/fastener points for
  tool-light replacement.

## Engineering challenges & dependencies
1. **Expression actuation:** silicone resists deformation; many small, strong,
   quiet actuators and careful anchor-point design are required. Dependency:
   actuator packaging + control bandwidth. Risk: **high**.
2. **Uncanny valley:** cosmetic realism is a long iterative art/engineering
   loop; not a solved deliverable.
3. **Durability & cleaning:** silicone tears/stains; define cleaning agents and
   replacement interval (see `docs/maintenance/`). Unknown until tested.
4. **Thermal/comfort:** actuators behind the face generate heat; must not
   deform or discolour skin.
5. **Safety:** face mechanisms are low-force but still pinch risks near eyes/jaw;
   enforce travel limits and covers.

## Honest conclusion
Treat the skin/expression system as **R&D**, commissioned only after the head
mechanism (eyes/eyelids/jaw) works reliably on the bench. Do not promise
photorealistic skin or full facial expressions as delivered capability.
