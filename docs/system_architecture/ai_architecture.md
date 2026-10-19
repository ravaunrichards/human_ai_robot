# AI, Speech, Vision & Motion Architecture

**Status:** interfaces implemented; real backends are optional and not bundled.

## Conversation
- `ConversationProvider` is the adapter contract (`generate(messages) -> str`).
- Providers shipped: `LocalLLMProvider` (offline-capable, needs an injected
  runner such as llama.cpp/Ollama), `OnlineProvider` (optional, requires
  internet + API key), `EchoProvider` (always-available offline fallback).
- `ConversationManager` tries providers in order and **falls back** to the next
  available one, guaranteeing a response path even with no model/no network.
- Providers return **text only**. They never return motor commands.

### Local model options (not bundled)
- llama.cpp / GGUF models, Ollama, or an on-device transformers runtime.
- Wire via `LocalLLMProvider(runner=callable)`.

### Online providers (optional)
- Any HTTP LLM via an injected `client` callable + `*_API_KEY` from env.
- `requires_internet = True`; must never gate safety.

## Speech
- `SpeechToText`, `TextToSpeech`, `VoiceActivityDetector`, `AudioDevice`.
- Offline no-op implementations ship for development/tests.
- Recommended offline engines (install separately): **Vosk** or
  **whisper.cpp** (STT), **Piper** or **espeak-ng** (TTS), **WebRTC VAD** or
  **Silero** (VAD), **sounddevice/PortAudio** (I/O).
- `EnergyVAD` is a dependency-free baseline included and tested.

## Vision
- `Camera` interface + `NullCamera` for development.
- `PerceptionLayer` runs a pluggable list of detectors; none bundled, so the
  honest default is “no perception backend installed”.
- **Privacy by default:** perception off, face **recognition not implemented**,
  frames not persisted. Only optional face *detection* behind an explicit flag.
- Recommended backends (install separately): OpenCV, a person/object detector
  (e.g. YOLO/MediaPipe), run **on-device** where possible.

## Motion planning
- `MotionRequest` / `JointCommand` are strict, validated data models.
- `MotionPlanner.validate()` rejects unknown joints, out-of-range targets and
  over-velocity commands.
- `MotionPlanner.submit()` dispatches to hardware **only** when validation
  passes **and** the safety gate is open (`enable_motion()` succeeded).
- A language model cannot bypass this: it has no path to `send_joint_commands`.

## Diagnostics
- Structured JSON logging (`diagnostics.logging_setup`).
- `FaultLog` + `FaultCode` enum; `HealthMonitor` with named checks.
- Health checks never raise (exceptions are treated as failures).

## Which features need internet?
| Feature | Internet required? |
|---------|--------------------|
| Safety (limits, watchdog, e-stop, faults) | **No — never** |
| Local conversation / echo fallback | No |
| Online conversation provider | Yes |
| Offline STT/TTS (Vosk/whisper.cpp/Piper) | No |
| Cloud STT/TTS (optional) | Yes |
| On-device vision | No |
