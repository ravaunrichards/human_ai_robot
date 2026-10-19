# Firmware (Starter Stubs — NOT flashed or tested)

**Status: STARTER / HARDWARE-NEUTRAL.** No specific MCU has been selected, so
this is portable C that compiles as host-side logic for review and unit reasoning
but is **not** built for or flashed to any board, and **not** tested on hardware.
It documents the intended real-time structure and the safety responsibilities of
each controller.

## Controllers
- `safety_controller/` — independent safety MCU: E-STOP monitoring, power
  contactor control, independent watchdog, thermal/current fault inputs. Must
  function even if the motion MCU and host are dead.
- `motion_controller/` — real-time joint coordination, host heartbeat watchdog,
  **re-validates joint limits** (defence in depth), owns the comms link.
- `joint_modules/` — per-joint closed-loop control template.
- `sensor_interfaces/` — encoder/IMU/temp/current acquisition template.

## Shared protocol
`motion_controller/protocol.h` mirrors the framing + CRC in
`software/hardware_interfaces/protocol.py` so host and firmware share one wire
format. The CRC implementation is identical (CRC-16/CCITT, poly 0x1021).

## Safety rules encoded here (as intent)
- Drive stays disabled until explicitly enabled AND the safety MCU reports OK.
- Watchdog expiry → ramp to safe hold → disable drive.
- Any limit breach, over-current or over-temp → fault → safe state.
- The host can request motion but cannot force drive power on.

## Next engineering step
Select the safety MCU, motion MCU and joint drivers (see BOM), then port these
stubs to the vendor HAL, freeze the joint table, and bring up on the bench per
`docs/safety/commissioning.md`.
