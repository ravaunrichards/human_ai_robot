import pytest

from software.hardware_interfaces.protocol import (
    Frame,
    MSG_JOINT_CMD,
    crc16_ccitt,
    decode,
)


def test_encode_decode_roundtrip():
    f = Frame(msg_type=MSG_JOINT_CMD, seq=7, payload=b"\x01\x02\x03")
    raw = f.encode()
    out = decode(raw)
    assert out is not None
    assert out.msg_type == MSG_JOINT_CMD
    assert out.seq == 7
    assert out.payload == b"\x01\x02\x03"


def test_incomplete_frame_returns_none():
    f = Frame(MSG_JOINT_CMD, 1, b"abc")
    raw = f.encode()
    assert decode(raw[:-1]) is None


def test_corrupt_crc_raises():
    f = Frame(MSG_JOINT_CMD, 1, b"abc")
    raw = bytearray(f.encode())
    raw[-1] ^= 0xFF  # corrupt crc
    with pytest.raises(ValueError):
        decode(bytes(raw))


def test_bad_start_bytes_raise():
    with pytest.raises(ValueError):
        decode(b"\x00\x00\x01\x02\x03\x04\x05\x06\x07")


def test_payload_too_long_rejected():
    with pytest.raises(ValueError):
        Frame(MSG_JOINT_CMD, 1, b"x" * 256).encode()


def test_crc_is_deterministic():
    assert crc16_ccitt(b"123456789") == crc16_ccitt(b"123456789")
