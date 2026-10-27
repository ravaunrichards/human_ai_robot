# Beulah & Prudence 3D Display Update

## Included
- Replaced broken vendor-hosted photo display with an integrated interactive `<model-viewer>` stage.
- Added full 3D model rotation/zoom controls, reset-view and animation selection when clips are present.
- Added Beulah / Prudence selector buttons.
- Added a same-origin model endpoint that fetches only two allowlisted, CC0 GLB files from Innerscene and caches them in `/tmp/human_ai_robot_models`; arbitrary proxy URLs are not accepted.
- Models are named by selected companion in the UI, but are licensed base characters, not verified likenesses of the selected Nova Beige product dolls.
- Physical robot motion remains disabled. No GitHub repository or Render service was changed.

## Asset sources and license
- Maya animated 3D human model (Beulah display profile): https://www.innerscene.com/tools/library/3d-parts/locomotion-collection-maya-3d-person-animated-1499b2fd
- Harper animated 3D human model (Prudence display profile): https://www.innerscene.com/tools/library/3d-parts/locomotion-collection-harper-3d-person-animated-797e1e2a
- Innerscene labels both GLB assets public-domain CC0. The source pages describe rigged human models with animation clips.
- The Google `<model-viewer>` runtime is loaded from Google's hosted libraries at version 4.4.0. It requires an internet connection unless later vendored locally.

## Important limitations
- The 3D characters are not reconstructed from Beulah's and Prudence's product photos and must not be represented as exact likenesses. Creating faithful likenesses requires additional 3D modeling/generation and reference views.
- Model files are downloaded by the server on first request. The model host must remain accessible and the server must have outbound HTTPS access. Model fetch is not verified in the local build environment because its DNS/network is restricted.
- Provider API connectivity and live AI responses are separate and are not newly verified here.
