# Build verification — interactive 3D companion display

## Automated checks

- `node --check web/app.js` — passed.
- `python -m py_compile software/web_server.py software/virtual_ai_service.py` — passed.
- `python -m unittest discover -s tests -v` — **8/8 tests passed**.
- The 3D-route tests verify that an allowlisted GLB is served with `model/gltf-binary`, cached after first fetch, and that unknown model names return 404 without triggering a network fetch.
- ZIP archive integrity is checked after packaging.

## What is built

- Integrated Google `<model-viewer>` stage with user-controlled rotation and zoom.
- Beulah / Prudence selection, camera reset, animation picker populated from the actual model's available animation clips, loading feedback and error display.
- Two fixed same-origin model endpoints with a server-side cache and a 32 MiB payload cap.
- Physical robot movement remains disabled.

## Not verified in this build environment

- Outbound DNS/network access from this container is restricted, so the real upstream GLB files could not be downloaded or rendered here. The deployed server needs outbound HTTPS access to Innerscene; the browser needs access to Google's hosted `<model-viewer>` runtime. The user-visible stage shows a clear error and retry control if the assets cannot load.
- The two CC0 human models are animation-ready base assets, **not exact 3D likenesses** reconstructed from Beulah's and Prudence's product images. The viewer integration is built; faithful likeness creation remains a separate 3D modeling task.
- Provider/API connectivity and live AI replies were not newly verified.

## External repository / hosting

No GitHub repository was changed and no Render service was changed or deployed.
