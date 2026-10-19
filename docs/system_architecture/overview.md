# System Architecture Overview

**Status:** design baseline. Interfaces are implemented in `software/`; real-time
firmware and hardware are proposals.

## Design goals
1. **Safety is independent of AI and internet.** All time-critical and
   safety-critical behaviour lives in local real-time controllers.
2. **Modularity.** Every external capability (LLM, STT, TTS, VAD, camera,
   perception, actuator driver) sits behind a replaceable interface.
3. **Honest status.** Nothing unverified is presented as validated or safe.

## Layers
### 1. High-level computer (non-real-time)
- Runs the Python stack in `software/`.
- Responsibilities: conversation, speech, vision/perception, behaviour, logging,
  health, and producing **bounded motion intentions**.
- Explicitly **not** trusted for safety timing. It can crash or lose network
  without endangering anyone.

### 2. Real-time control layer (firmware)
- `firmware/safety_controller` — independent safety MCU: monitors e-stop,
  power rails, watchdog, temperature; can cut actuator power without the host.
- `firmware/motion_controller` — coordinates joint set-points, enforces limits
  again at the controller, runs the host heartbeat watchdog.
- `firmware/joint_modules` — per-joint closed-loop position/velocity control.
- `firmware/sensor_interfaces` — encoders, IMU, temperature, current, F/T.

### 3. Hardware (physical)
- Frame, actuators, sensors, power, enclosures, skin. See `hardware/` and
  `docs/mechanical_design/`.

## Data flow & trust boundaries
```
untrusted text  ->  Conversation (LLM)      # text in, text out ONLY
                      |
   behaviour layer translates intent -> MotionRequest (bounded)
                      |
              MotionPlanner.validate()       # reject malformed/out-of-range
                      | (dispatch only if safety gate open)
     Comm protocol (CRC-framed messages, software/hardware_interfaces/protocol.py)
                      |
     Motion MCU  <-- re-validates limits -->  Joint modules
          ^
          |  independent
     Safety MCU + hardware E-STOP + power isolation
```
Key rule: **the LLM output never crosses into the motion path as commands.** A
separate behaviour layer emits only bounded, named intentions, which become
`MotionRequest` objects validated against joint limits.

## Repository structure
```
human_ai_robot/
  README.md LICENSE SECURITY.md CONTRIBUTING.md pyproject.toml .gitignore .env.example
  docs/            engineering documentation (status-labelled)
  hardware/        mechanical notes + CAD sources (per subsystem)
  firmware/        real-time controller starter code + specs
  software/        Python AI-computer stack (runnable, tested)
  configuration/   joint limits, calibration, sensors, power configs
  tests/           unit / integration / safety / hardware (hardware skipped)
  tools/           setup / calibration / diagnostics / scripts
```

## Offline operation
If internet or the online LLM fails: conversation falls back to a local model
and then an offline echo; speech/vision degrade to offline/no-op; and **all**
safety functions (limits, watchdog, e-stop, fault handling) are unaffected
because they do not depend on the host or network. Features that require
internet are limited to the optional online AI provider and any cloud speech.
