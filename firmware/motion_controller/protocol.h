/*
 * protocol.h - shared wire format (host <-> controllers).
 * Mirrors software/hardware_interfaces/protocol.py.
 * CRC-16/CCITT, poly 0x1021, init 0xFFFF. Little-endian CRC on the wire.
 * STATUS: hardware-neutral starter; not flashed or tested on a target.
 */
#ifndef HAR_PROTOCOL_H
#define HAR_PROTOCOL_H

#include <stdint.h>
#include <stddef.h>

#define HAR_START0 0xAAu
#define HAR_START1 0x55u

#define HAR_MSG_HEARTBEAT 0x01u
#define HAR_MSG_JOINT_CMD 0x02u
#define HAR_MSG_STATE     0x03u
#define HAR_MSG_ESTOP     0x04u
#define HAR_MSG_FAULT     0x05u

static inline uint16_t har_crc16_ccitt(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFFu;
    for (size_t i = 0; i < len; ++i) {
        crc ^= (uint16_t)data[i] << 8;
        for (int b = 0; b < 8; ++b) {
            if (crc & 0x8000u) crc = (uint16_t)((crc << 1) ^ 0x1021u);
            else               crc = (uint16_t)(crc << 1);
        }
    }
    return crc;
}

/* Encode a frame into out (must hold 5 + len + 2 bytes). Returns total size
 * or 0 on error (len > 255). */
static inline size_t har_encode(uint8_t msg_type, uint8_t seq,
                                const uint8_t *payload, uint8_t len,
                                uint8_t *out, size_t out_cap) {
    if (len > 255u) return 0;
    size_t total = (size_t)(5 + len + 2);
    if (out_cap < total) return 0;
    out[0] = HAR_START0; out[1] = HAR_START1;
    out[2] = msg_type; out[3] = seq; out[4] = len;
    for (uint8_t i = 0; i < len; ++i) out[5 + i] = payload[i];
    uint16_t crc = har_crc16_ccitt(&out[2], (size_t)(3 + len));
    out[5 + len] = (uint8_t)(crc & 0xFFu);
    out[6 + len] = (uint8_t)((crc >> 8) & 0xFFu);
    return total;
}

/* Returns 1 if a complete valid frame is at buf[0..]; sets *consumed.
 * Returns 0 if incomplete, -1 on CRC/format error. */
static inline int har_decode(const uint8_t *buf, size_t avail,
                             uint8_t *msg_type, uint8_t *seq,
                             const uint8_t **payload, uint8_t *len,
                             size_t *consumed) {
    if (avail < 7u) return 0;
    if (buf[0] != HAR_START0 || buf[1] != HAR_START1) return -1;
    uint8_t l = buf[4];
    size_t end = (size_t)(5 + l);
    if (avail < end + 2u) return 0;
    uint16_t rx = (uint16_t)buf[end] | ((uint16_t)buf[end + 1] << 8);
    uint16_t calc = har_crc16_ccitt(&buf[2], (size_t)(3 + l));
    if (rx != calc) return -1;
    *msg_type = buf[2]; *seq = buf[3]; *payload = &buf[5]; *len = l;
    *consumed = end + 2u;
    return 1;
}

#endif /* HAR_PROTOCOL_H */
