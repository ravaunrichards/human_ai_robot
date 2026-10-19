"""Communication protocol helpers (AI computer <-> local controllers).

This is a reference framing + checksum scheme for a serial / UART / CAN
bridge between the high-level computer and the real-time safety and motion
controllers. The real transport is intentionally abstract; only the
message encoding/decoding and CRC are implemented here so both sides can
share one source of truth.

Frame layout (little-endian):
  0xAA 0x55 | msg_type(1) | seq(1) | length(1) | payload(length) | crc16(2)

See docs/system_architecture/communication_protocol.md for the full spec.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Optional

START = b"\xAA\x55"

MSG_HEARTBEAT = 0x01
MSG_JOINT_CMD = 0x02
MSG_STATE = 0x03
MSG_ESTOP = 0x04
MSG_FAULT = 0x05


def crc16_ccitt(data: bytes, poly: int = 0x1021, init: int = 0xFFFF) -> int:
    crc = init
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc & 0xFFFF


@dataclass
class Frame:
    msg_type: int
    seq: int
    payload: bytes

    def encode(self) -> bytes:
        if not (0 <= self.msg_type <= 0xFF):
            raise ValueError("msg_type out of range")
        if not (0 <= self.seq <= 0xFF):
            raise ValueError("seq out of range")
        if len(self.payload) > 0xFF:
            raise ValueError("payload too long (max 255 bytes)")
        body = struct.pack("BBB", self.msg_type, self.seq, len(self.payload)) + self.payload
        crc = crc16_ccitt(body)
        return START + body + struct.pack("<H", crc)


def decode(buffer: bytes) -> Optional[Frame]:
    """Decode a single frame from the start of ``buffer``.

    Returns None if the buffer does not contain a complete, valid frame.
    Raises ValueError on CRC mismatch (corrupt frame) so callers can log
    a communication fault rather than silently acting on bad data.
    """
    if len(buffer) < 7:
        return None
    if buffer[:2] != START:
        raise ValueError("bad start bytes")
    msg_type, seq, length = struct.unpack("BBB", buffer[2:5])
    end = 5 + length
    if len(buffer) < end + 2:
        return None
    payload = buffer[5:end]
    (crc_rx,) = struct.unpack("<H", buffer[end:end + 2])
    crc_calc = crc16_ccitt(buffer[2:end])
    if crc_rx != crc_calc:
        raise ValueError(f"CRC mismatch: rx={crc_rx:#06x} calc={crc_calc:#06x}")
    return Frame(msg_type=msg_type, seq=seq, payload=payload)
