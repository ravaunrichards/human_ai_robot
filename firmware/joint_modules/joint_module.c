/*
 * joint_module.c - per-joint closed-loop control (STARTER STUB).
 * STATUS: hardware-neutral; not flashed or tested.
 *
 * A joint module tracks a validated set-point from the motion controller
 * using a simple position loop with a velocity clamp. The real controller
 * must add current/torque limiting, backlash handling and driver faults.
 */
#include <stdint.h>

extern float hal_read_position_deg(uint8_t jid);
extern void  hal_command_velocity_dps(uint8_t jid, float vel_dps);
extern int   hal_driver_faulted(uint8_t jid);

typedef struct { float kp; float max_vel_dps; } joint_gains_t;

static joint_gains_t g_gains = { .kp = 2.0f, .max_vel_dps = 30.0f };

static float clampf(float v, float lo, float hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

/* target_deg is assumed already range-validated by motion_controller. */
void joint_update(uint8_t jid, float target_deg) {
    if (hal_driver_faulted(jid)) { hal_command_velocity_dps(jid, 0.0f); return; }
    float pos = hal_read_position_deg(jid);
    float err = target_deg - pos;
    float vel = clampf(g_gains.kp * err, -g_gains.max_vel_dps, g_gains.max_vel_dps);
    hal_command_velocity_dps(jid, vel);
}

void joint_safe_hold(uint8_t jid) { hal_command_velocity_dps(jid, 0.0f); }
