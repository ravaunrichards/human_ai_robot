# Electrical Design & Power Architecture (Conceptual)

**STATUS: CONCEPTUAL.** No connector pinouts or wiring tables here are matched to
final component datasheets. Do not treat any diagram as build-ready. All
ratings must be confirmed against the actual selected parts before wiring.

## 1. Power source & distribution (proposed)
- Options: (a) tethered DC bench PSU for commissioning (**recommended first**),
  (b) battery pack for untethered operation (later stage).
- Two separated domains:
  - **Logic power** (compute, MCUs, sensors): e.g. 5 V / 12 V regulated.
  - **Actuator power** (motor bus): e.g. 24–48 V, high current.
- Logic and actuator grounds joined at a single star point; document returns.

## 2. Circuit protection
- Main fuse/breaker on the actuator bus sized to wiring + worst-case stall
  (value TBD from actuator datasheets).
- Per-branch fusing for joint groups.
- Logic rail separately fused; reverse-polarity and inrush protection.

## 3. Emergency stop & isolation (MANDATORY, independent)
- A hardware **E-STOP** latching mushroom switch in the actuator-power path
  (via contactor/relay) that physically removes motor-bus power.
- E-STOP is **independent of software and the host computer**.
- A separate **power-isolation** disconnect for service.
- The safety MCU can also drop the contactor, but the manual E-STOP must work
  even if all firmware is dead. See `docs/safety/`.

## 4. Logic vs actuator separation
- Separate converters; opto/galvanic isolation on control signals crossing from
  logic to high-power drivers where appropriate.

## 5. Controller / actuator / encoder / sensor interfaces (proposed)
- Motion MCU ↔ joint drivers: CAN FD or RS-485 bus (TBD).
- Encoders: absolute (SPI/BiSS) preferred for joints that must know position at
  power-up; incremental acceptable with homing.
- Sensors: IMU (SPI/I2C), joint temperature, bus current sense, foot F/T
  (later).

## 6. Camera / mic / speaker / network
- Camera(s): USB/MIPI-CSI to the host computer.
- Microphones: USB or I2S array to host.
- Speaker: amplifier from host audio out.
- Network: Wi-Fi/Ethernet on host **only**; never on the safety path.

## 7. Grounding, shielding, connectors
- Shielded cable for encoders and signal buses; shield grounded at one end.
- Keyed, lockable connectors; label every connector per
  `docs/wiring/connector_identification.md`.

## 8. Battery safety (if batteries used)
- Protected pack with BMS: over/under-voltage, over-current, cell balancing,
  temperature cutoff. Charging on a non-flammable surface, supervised.
- No battery part is selected or validated here.

## 9. Block diagram
See `docs/electrical_design/block_diagram.md` (ASCII conceptual diagram).

## Honest limitation
Until specific actuators, drivers and a controller are selected, voltages,
currents and pinouts cannot be finalised. The wiring tables in `docs/wiring/`
are templates with placeholders marked `TBD`.
