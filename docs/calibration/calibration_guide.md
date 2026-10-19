# Calibration Guide (Preliminary)

**Status: PRELIMINARY.** Procedures assume hardware that does not yet exist.
All calibration must be done on fixtures, de-risked per `docs/safety/`.

## Joint zero / range calibration
1. Mount joint in a secure fixture (off-body for early stages).
2. With drive **disabled**, move the joint by hand to each mechanical stop;
   record encoder counts.
3. Compute mechanical range; set **verified** min/max in
   `configuration/joint_limits/` leaving a safety margin inside the hard stops.
4. Only then set `"verified": true` for that joint.
5. Re-run `tools/calibration/validate_limits.py` to sanity-check the file.

## Encoder homing
- Absolute encoders: record offset between encoder zero and mechanical zero.
- Incremental encoders: define a repeatable homing routine to a known stop at
  low speed (supervised).

## Centre-of-mass check
- Use `tools/calibration/com_estimator.py` with real per-part masses to update
  the CoM budget as parts are installed.

## Sensor calibration
- IMU: static bias capture while level and still.
- Current/temperature: verify against a reference meter.

## Records
Store measured values as `configuration/calibration/measured_*.json` (git-ignored)
and summarise verified limits back into the tracked limits file.
