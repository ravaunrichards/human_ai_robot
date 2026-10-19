# Wiring Tables (TEMPLATE — placeholders)

**STATUS: TEMPLATE.** Pin assignments, voltages and currents are `TBD` until the
exact components are selected and their datasheets consulted. Do NOT wire from
this table. Inventing pinouts is explicitly prohibited by the project rules.

## How to use
Fill one row per physical connection after selecting parts. Keep the
`status` column honest (`TBD`, `candidate`, `confirmed`).

## Actuator bus (per joint) — template
| From | To | Signal | Connector | Voltage | Current | Pin | Status |
|------|----|--------|-----------|---------|---------|-----|--------|
| Fused bus | Joint driver N | V+ | TBD | TBD | TBD | TBD | TBD |
| Fused bus | Joint driver N | GND | TBD | 0V | TBD | TBD | TBD |
| Motion MCU | Joint driver N | CAN_H | TBD | — | — | TBD | TBD |
| Motion MCU | Joint driver N | CAN_L | TBD | — | — | TBD | TBD |
| Joint driver N | Motor N | phase U/V/W | TBD | TBD | TBD | TBD | TBD |
| Encoder N | Joint driver N | SPI/BiSS | TBD | 3V3/5V | low | TBD | TBD |

## Logic & sensors — template
| From | To | Signal | Connector | Voltage | Current | Pin | Status |
|------|----|--------|-----------|---------|---------|-----|--------|
| Logic PSU | Host PC | V+/GND | TBD | TBD | TBD | TBD | TBD |
| Host PC | Camera | USB/CSI | TBD | 5V | TBD | TBD | TBD |
| Host PC | Mic array | USB/I2S | TBD | 5V/3V3 | low | TBD | TBD |
| Host PC | Amp->Speaker | audio | TBD | — | — | TBD | TBD |
| Safety MCU | Contactor coil | drive | TBD | TBD | TBD | TBD | TBD |
| E-STOP switch | Contactor | NC loop | TBD | TBD | TBD | TBD | TBD |

## Safety loop — template
| Element | Function | Normally | Status |
|---------|----------|----------|--------|
| Manual E-STOP | opens contactor coil loop | closed | TBD |
| Safety MCU relay | can also open loop | closed | TBD |
| Door/service interlock (optional) | opens loop when panel removed | closed | TBD |
