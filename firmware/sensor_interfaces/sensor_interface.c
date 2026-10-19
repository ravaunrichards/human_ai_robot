/*
 * sensor_interface.c - sensor acquisition template (STARTER STUB).
 * STATUS: hardware-neutral; not flashed or tested.
 *
 * Aggregates encoder, IMU, temperature and current readings and exposes a
 * compact status for the STATE frame. Over-temp / over-current thresholds
 * feed the safety MCU fault inputs.
 */
#include <stdint.h>

extern float hal_encoder_deg(uint8_t jid);
extern float hal_temp_c(uint8_t idx);
extern float hal_current_a(uint8_t idx);

#define TEMP_LIMIT_C   85.0f   /* placeholder; set from datasheets */
#define CURRENT_LIMIT_A 20.0f  /* placeholder; set from bus design */

typedef struct { int over_temp; int over_current; } sensor_faults_t;

sensor_faults_t sensor_scan(uint8_t n_temp, uint8_t n_curr) {
    sensor_faults_t f = {0, 0};
    for (uint8_t i = 0; i < n_temp; ++i) if (hal_temp_c(i) > TEMP_LIMIT_C) f.over_temp = 1;
    for (uint8_t i = 0; i < n_curr; ++i) if (hal_current_a(i) > CURRENT_LIMIT_A) f.over_current = 1;
    return f;
}
