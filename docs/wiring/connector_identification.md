# Connector Identification & Labelling (Template)

**Status: TEMPLATE.** Populate once parts are selected.

## Labelling scheme (proposed)
`<domain>-<subsystem>-<index>` e.g. `ACT-ARM_L-03`, `LOG-HEAD-01`, `SAFE-ESTOP-01`.

- `domain`: ACT (actuator power), LOG (logic), SIG (signal bus), SAFE (safety).
- Every connector gets a printed label at both ends.
- Keyed/polarised connectors mandatory on power.
- Maintain a connector register (CSV) alongside this file once populated.

## Register template
| Label | From | To | Type | Keyed | Shield | Status |
|-------|------|----|------|-------|--------|--------|
| ACT-ARM_L-03 | fused bus | L elbow driver | TBD | yes | n/a | TBD |
| SIG-SPINE-01 | Motion MCU | CAN backbone | TBD | yes | yes | TBD |
| SAFE-ESTOP-01 | E-STOP | contactor | TBD | yes | n/a | TBD |
