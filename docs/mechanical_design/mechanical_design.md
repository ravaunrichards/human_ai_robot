# Mechanical Design (Preliminary)

**STATUS: PRELIMINARY — NOT VERIFIED.** Every dimension, mass and torque below is
an engineering assumption for planning. None is validated by analysis or test.
Do not fabricate load-bearing parts from these numbers without FEA and a
qualified mechanical engineer's review.

## 1. Body dimensions & proportion targets (preliminary)
Adult female-presenting, standing figure. Targets, to be verified:
| Parameter | Target | Basis / note |
|-----------|--------|--------------|
| Standing height | 1.65 m | design target |
| Total mass | 45–65 kg (goal) | **optimistic**; real humanoids often exceed this |
| Shoulder width | 0.37 m | proportion target |
| Reach (fingertip) | ~0.70 m per arm | proportion target |
| CoM height (standing) | ~0.95 m | to be computed from parts |

Proportions use a nominal 7.5-head canon as a starting aesthetic target; the
mechanical envelope takes priority over cosmetic proportion.

## 2. Skeletal frame, materials, manufacturing (proposed)
- Primary structure: 6061-T6 aluminium machined brackets + carbon/aluminium
  tubes; high-load joints (hip/knee) in 7075 or steel.
- Methods: CNC machining, sheet bending, selective 3D-printed covers (not
  load-bearing).
- **Challenge:** mass vs. stiffness vs. actuator torque is the central trade;
  not resolved.

## 3. Degrees of freedom (proposed layout)
See `docs/mechanical_design/joint_dof.md` for the full DOF table. Summary: head
/ neck (3), eyes (2) + eyelids (2) + jaw (1), each arm (shoulder 3, elbow 1,
wrist 2), hands (functional vs decorative distinguished), each leg (hip 3, knee
1, ankle 2). The shipped placeholder limits cover a reduced, representative set.

## 4. Actuator selection criteria (method, not final parts)
For each joint estimate: peak torque = (mass beyond joint) x g x (lever arm) x
safety factor (>=2). Add dynamic terms for accelerated limbs. Choose actuator
by continuous torque >= gravity-hold torque at worst pose, and peak torque >=
dynamic peak. Consider gearing backlash, backdrivability (safety), duty cycle
and thermal rise. **No torque value here is validated.**

Worked example method (illustrative, NOT a spec): a 3 kg forearm+hand with CoM
0.18 m from the elbow needs gravity-hold torque ~ 3 x 9.81 x 0.18 ≈ 5.3 N·m;
with SF 2 and dynamics, size for >= ~12–15 N·m continuous. Verify with real
mass properties from CAD.

## 5. Mass & centre-of-mass method
Compute per-part mass from CAD density x volume; aggregate CoM = Σ(m_i r_i)/Σm_i.
Maintain a running CoM budget as parts are selected. See
`tools/calibration/com_estimator.py` for a reproducible estimator skeleton.

## 6. Stability, support, fall prevention
- Until balance is commissioned, the robot must be **externally supported**
  (gantry/stand) — see safety docs. Free-standing balance and walking are
  **separate, high-risk commissioning stages**, not assumed achievable.

## 7. Cable routing, pinch points, thermal
- Route cabling through joint centres with service loops; document pinch zones
  and add covers. Hot actuators/drivers need airflow or heatsinking; add
  temperature sensors feeding the safety MCU.

## 8. Exterior shell & skin
- Replaceable panels on captive fasteners; service-access covers over
  electronics and e-stop. Skin system: see `docs/mechanical_design/skin_system.md`
  — realistic silicone is **not assumed trivial**.

## 9. Assembly sequence & inspection
See `docs/assembly/assembly_sequence.md` and the inspection checklist there.

## 10. CAD / parametric source
See `hardware/cad/` — a reproducible parametric script generates a schematic
skeleton (envelope + joint frames), explicitly a layout aid, not a
manufacturing model.
