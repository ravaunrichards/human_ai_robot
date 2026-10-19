/*
 * safety_controller.c - independent safety MCU logic (STARTER STUB).
 * STATUS: hardware-neutral; not flashed or tested. Vendor HAL calls are
 * stubbed. This MUST run on an MCU independent of the host and motion MCU.
 *
 * Responsibilities:
 *   - Monitor the manual E-STOP loop (hardware-latched upstream too).
 *   - Hold the actuator-bus contactor CLOSED only while all conditions are OK.
 *   - Independent watchdog on the motion MCU heartbeat.
 *   - Trip on over-temperature / over-current fault inputs.
 *
 * SAFETY: default state is contactor OPEN (no actuator power).
 */
#include <stdint.h>

/* ---- HAL stubs (replace with vendor HAL on the selected MCU) ---- */
extern int   hal_estop_loop_closed(void);     /* 1 = E-STOP not pressed */
extern int   hal_overtemp_fault(void);        /* 1 = over temperature */
extern int   hal_overcurrent_fault(void);     /* 1 = over current */
extern uint32_t hal_millis(void);
extern void  hal_set_contactor(int closed);   /* close/open actuator-bus power */
extern int   hal_motion_heartbeat_seen(void); /* 1 if heartbeat since last clear */
extern void  hal_clear_motion_heartbeat(void);

#define SAFETY_WATCHDOG_MS 200u

typedef struct {
    uint32_t last_hb_ms;
    int      tripped;
} safety_state_t;

static safety_state_t g_state;

void safety_init(void) {
    g_state.last_hb_ms = hal_millis();
    g_state.tripped = 1;            /* start tripped: power OFF by default */
    hal_set_contactor(0);
}

static int conditions_ok(void) {
    if (!hal_estop_loop_closed()) return 0;   /* E-STOP pressed */
    if (hal_overtemp_fault())     return 0;
    if (hal_overcurrent_fault())  return 0;
    uint32_t now = hal_millis();
    if (hal_motion_heartbeat_seen()) {
        g_state.last_hb_ms = now;
        hal_clear_motion_heartbeat();
    }
    if ((now - g_state.last_hb_ms) > SAFETY_WATCHDOG_MS) return 0; /* host/motion dead */
    return 1;
}

/* Call from a high-priority periodic interrupt. */
void safety_tick(void) {
    if (!conditions_ok()) {
        g_state.tripped = 1;
        hal_set_contactor(0);      /* remove actuator-bus power */
        return;
    }
    /* All OK: a tripped state requires an explicit external reset elsewhere
     * before power is restored (not auto-cleared here on purpose). */
    if (!g_state.tripped) {
        hal_set_contactor(1);
    }
}

/* Explicit, deliberate reset (e.g. operator button) after conditions are OK. */
void safety_reset(void) {
    if (conditions_ok()) {
        g_state.tripped = 0;
    }
}
