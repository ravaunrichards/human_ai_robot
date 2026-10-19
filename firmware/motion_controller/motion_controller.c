/*
 * motion_controller.c - real-time motion MCU logic (STARTER STUB).
 * STATUS: hardware-neutral; not flashed or tested.
 *
 * Responsibilities:
 *   - Receive JOINT_CMD frames from the host, verify CRC.
 *   - RE-VALIDATE every target against the local limit table (defence in
 *     depth; the host already validated once).
 *   - Enforce a host-heartbeat watchdog: on expiry, ramp to safe hold and
 *     disable drive.
 *   - Forward only validated set-points to joint modules.
 *   - Drive power is gated by the independent safety MCU; this MCU cannot
 *     force power on.
 */
#include <stdint.h>
#include "protocol.h"

#define MOTION_WATCHDOG_MS 100u
#define MAX_JOINTS 24

typedef struct { int16_t min_cdeg, max_cdeg; uint16_t max_vel_cdps; uint8_t verified; } joint_limit_t;

extern uint32_t hal_millis(void);
extern void hal_emit_heartbeat_to_safety(void);
extern void hal_set_joint_setpoint(uint8_t joint_id, int16_t pos_cdeg, uint16_t vel_cdps);
extern void hal_disable_drive(void);

static joint_limit_t g_limits[MAX_JOINTS];  /* loaded from verified config */
static uint32_t g_last_host_ms;
static int g_drive_enabled;

void motion_init(void) {
    g_last_host_ms = hal_millis();
    g_drive_enabled = 0;               /* disabled by default */
    hal_disable_drive();
}

static int limit_ok(uint8_t jid, int16_t pos, uint16_t vel) {
    if (jid >= MAX_JOINTS) return 0;
    joint_limit_t *l = &g_limits[jid];
    if (!l->verified) return 0;        /* never move an unverified joint */
    if (pos < l->min_cdeg || pos > l->max_cdeg) return 0;
    if (vel > l->max_vel_cdps) return 0;
    return 1;
}

/* Called when a validated JOINT_CMD payload arrives.
 * payload layout: N x { jid(u8), pos_cdeg(i16 LE), vel_cdps(u16 LE) } */
void motion_on_joint_cmd(const uint8_t *payload, uint8_t len) {
    g_last_host_ms = hal_millis();
    if (!g_drive_enabled) return;      /* ignore unless enabled */
    uint8_t off = 0;
    while ((uint8_t)(off + 5) <= len) {
        uint8_t jid = payload[off];
        int16_t pos = (int16_t)(payload[off+1] | (payload[off+2] << 8));
        uint16_t vel = (uint16_t)(payload[off+3] | (payload[off+4] << 8));
        if (limit_ok(jid, pos, vel)) {
            hal_set_joint_setpoint(jid, pos, vel);
        }
        /* out-of-range targets are silently dropped (safe); a FAULT frame
         * should also be emitted to the host in the full implementation. */
        off = (uint8_t)(off + 5);
    }
}

/* High-priority periodic tick. */
void motion_tick(void) {
    hal_emit_heartbeat_to_safety();
    if ((hal_millis() - g_last_host_ms) > MOTION_WATCHDOG_MS) {
        g_drive_enabled = 0;
        hal_disable_drive();           /* host lost: safe hold then disable */
    }
}

void motion_enable(int on) { g_drive_enabled = on ? 1 : 0; if(!on) hal_disable_drive(); }
