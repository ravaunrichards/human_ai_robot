# Privacy Controls (Cameras, Microphones, Data)

## Defaults (privacy-first)
- **Perception is OFF by default** (`PerceptionConfig.enabled = False`).
- **Face recognition is NOT implemented** in this repository. Only optional
  face *detection* exists, behind an explicit `allow_face_detection` flag, and
  no identity matching is provided.
- **No frames or audio are persisted** unless an operator explicitly sets
  `persist_frames=True` (and provides their own storage path/consent process).
- No vision/audio data leaves the device unless an operator wires an online
  provider; on-device models are recommended.

## Limitations (honest)
- Any real detection requires models that are **not bundled**; the default
  pipeline reports “no perception backend installed”.
- Microphone capture for speech uses offline no-op devices by default; a real
  mic requires explicit configuration.

## Operator responsibilities
- Obtain consent before recording identifiable people.
- Comply with local privacy law for any deployment.
- Keep perception disabled unless actively needed; prefer on-device processing.
