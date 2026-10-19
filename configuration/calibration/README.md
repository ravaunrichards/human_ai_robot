# Calibration configuration

Measured calibration from real hardware is stored here as
`measured_*.json` or `*.local.json` and is **git-ignored** (see `.gitignore`)
because it is machine-specific and must come from physical measurement.

See `docs/calibration/calibration_guide.md` for the procedure. Verified joint
ranges derived from calibration are written back into
`configuration/joint_limits/` with `"verified": true` per measured joint.
