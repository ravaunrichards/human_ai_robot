# Cinematic 3D display update

This update removes the bright/white fallback canvas from the character stage and applies a dark cinematic environment, larger full-body viewing area, improved tone mapping, shadows, exposure, and mobile sizing.

The 3D viewer remains interactive (rotate/zoom/reset) and reads available animation clips from the loaded GLB. Model files are fetched by the server from the configured external asset host and cached locally on that server.

## Important limitations
- This styling update does not magically increase mesh or texture fidelity. The included CC0 models are general rigged human base models, not verified likenesses of Beulah and Prudence.
- Model loading and photorealistic appearance were not visually verified in this environment because outbound access to the model host is restricted.
- The 3D model files are not bundled inside this ZIP; first successful server fetch requires outbound HTTPS to the configured asset host.
- No GitHub repository or Render service was changed.
