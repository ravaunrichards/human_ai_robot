# Communication Protocol: AI Computer <-> Local Controllers

**Status:** framing + CRC implemented and tested in
`software/hardware_interfaces/protocol.py`. Transport binding (UART/USB-CDC/CAN)
is a proposal to be finalised against the selected controller datasheets.

## Goals
- Deterministic, checksummed messages.
- Host is **advisory**: the motion/safety MCUs re-validate everything and run
  their own watchdog, so a corrupt or missing host message degrades safely.

## Frame format (little-endian)
```
0xAA 0x55 | msg_type(1) | seq(1) | length(1) | payload(length) | crc16_ccitt(2)
```
- `crc16_ccitt` covers `msg_type|seq|length|payload` (poly 0x1021, init 0xFFFF).
- Max payload 255 bytes.
- Decoder returns `None` for incomplete frames and **raises** on CRC mismatch
  so the receiver logs `COMM_LOST`/corrupt frame rather than acting on bad data.

## Message types
| id | name | direction | payload (proposed) |
|----|------|-----------|--------------------|
| 0x01 | HEARTBEAT | host->MCU, MCU->host | monotonic ms (u32) |
| 0x02 | JOINT_CMD | host->motion MCU | N x {joint_id(u8), pos_centideg(i16), vel_cdps(u16)} |
| 0x03 | STATE | MCU->host | per-joint pos/vel/current/temp, flags |
| 0x04 | ESTOP | either | reason code (u8) |
| 0x05 | FAULT | MCU->host | fault_code(u8), detail |

## Timing & watchdog (proposed, to validate)
- Host heartbeat: 50 Hz. Motion MCU watchdog timeout: 100 ms → ramp to safe
  hold, then disable drive. Safety MCU independent watchdog: 200 ms → cut
  actuator power.
- These numbers are **preliminary** and must be verified against actuator
  dynamics and the chosen bus latency.

## Joint id mapping
Joint names (see `configuration/joint_limits/`) map to compact `joint_id` bytes
in a table shared by host and firmware. The authoritative table will live in
`firmware/motion_controller/joint_table.h` once the DOF list is frozen.

## Safety notes
- JOINT_CMD is accepted by the motion MCU **only** when: drive enabled, e-stop
  clear, watchdog healthy, and each target within the MCU's own limit table.
- The host cannot enable drive power; that is a physical + safety-MCU decision.
