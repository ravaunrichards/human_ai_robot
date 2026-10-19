# Security & Safety Policy

This project has two kinds of risk: **physical safety** (a full-size humanoid
can injure people) and **software/information security** (API keys, remote AI,
cameras and microphones). Both are treated as first-class.

## Physical safety is the priority
See `docs/safety/` for the full safety case. Key invariants enforced in code:

- Real actuator motion is **disabled by default** and cannot be enabled without
  an explicit operator acknowledgement token **and** fully *verified* joint
  limits **and** an attached hardware interface.
- `simulation_only` mode makes real motion impossible regardless of other flags.
- The example code ships only a **simulated** hardware backend. No real motor
  driver is included.
- An independent, hardware emergency-stop is **mandatory** before any power is
  applied to actuators. Software safeguards never replace physical safeguards.

## Secrets handling
- API keys are read **only** from environment variables (any `*_API_KEY`).
- `.env` is git-ignored; only `.env.example` is committed.
- Keys are never written to logs. The structured logger whitelists fields.
- Do not place keys in config files, source, CAD, or BOM.

## Privacy (cameras & microphones)
- Perception is **off by default**.
- Face **recognition** is intentionally **not implemented** in this repository.
- Frames and audio are **not persisted** unless an operator explicitly opts in.
- See `docs/safety/privacy.md`.

## Network posture
- Safety-critical functions must never depend on the internet or an online LLM.
- Online AI is optional and behind replaceable adapters.
- The project binds no network services by default.

## Reporting
For a real deployment, add a monitored security contact here. Report suspected
safety defects by opening an issue labelled `safety` and halting physical
testing until reviewed by a qualified engineer.
