# software/ — AI-computer stack (runnable, tested)

Modular Python stack for the high-level (non-real-time) computer. No third-party
dependencies required for the core + tests.

| Package | Purpose |
|---------|---------|
| `conversation/` | provider interface + local/online/echo adapters + fallback manager |
| `speech/` | STT / TTS / VAD / audio-device interfaces (+ offline no-ops) |
| `vision/` | camera interface + privacy-first perception layer |
| `motion_planner/` | motion request models, joint limits, planner, safety gate |
| `diagnostics/` | structured logging, fault codes, health monitor |
| `hardware_interfaces/` | abstract HW contract, simulated backend, comm protocol |
| `configuration/` | layered config loader (API keys from env only) |
| `app.py` | entry point: `python -m software.app [--once]` |

Safety: nothing here enables real motor output. The default hardware backend is
a simulation; the motion planner is disabled by default. See `../docs/safety/`.
