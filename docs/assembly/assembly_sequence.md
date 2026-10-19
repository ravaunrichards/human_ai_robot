# Assembly Sequence & Inspection Checklist (Preliminary)

**STATUS: PRELIMINARY.** Sequence is a planning guide; it assumes parts not yet
fabricated. Perform all powered steps only under the staged commissioning in
`docs/safety/commissioning.md`, supervised, with the E-STOP tested first.

## Build order (mechanical)
1. Fabricate/verify frame segments (torso spine, pelvis, limb bones).
2. Install bearings and dry-fit joints; verify free travel and mechanical stops.
3. Mount actuators to joints **without power**; route and strain-relieve cables.
4. Install encoders; verify mechanical zero references.
5. Fit non-load-bearing panels loosely to check clearances; remove for wiring.
6. Mount electronics trays (host, MCUs, drivers), contactor and E-STOP.
7. Wire logic domain first; then actuator domain with bus **de-energised**.
8. Install head mechanism (eyes/eyelids/jaw) last; it is delicate.
9. Fit exterior panels and (later) face shell after bring-up.

## Inspection checklist (per subsystem, before any power)
- [ ] All fasteners torqued and threadlocked where required.
- [ ] No cable in a pinch/shear path; service loops present.
- [ ] Mechanical stops present and within intended travel.
- [ ] Encoder references documented.
- [ ] Connectors keyed, labelled, seated, strain-relieved.
- [ ] Logic and actuator grounds per star-point plan.
- [ ] Fuses installed and correctly rated (per final datasheets).
- [ ] E-STOP physically removes actuator-bus power (test de-energised, then at
      low voltage) BEFORE any joint is energised.
- [ ] Guards/covers over pinch points and the head mechanism.

## Hand-off gates
Do not proceed from one subsystem to the next until its inspection checklist is
signed off (see `docs/safety/signoff_record.md`).
