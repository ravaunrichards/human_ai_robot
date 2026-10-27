# Apply the 3D companion display to a local checkout

This ZIP is a **local build overlay**, not a completed change to your GitHub repository or any hosted website. I have not applied it to GitHub or Render. Before combining it with a repository, review the existing files and merge conflicts rather than blindly overwriting source.

## What changed

- `web/index.html`, `web/app.css`, and `web/app.js` now render interactive 3D adult human models using Google's `<model-viewer>` web component.
- `software/web_server.py` adds two fixed-name 3D asset routes and an on-server cache for the CC0 GLB models. It does not accept arbitrary URLs.
- `tests/test_3d_model_routes.py` covers the GLB response/cache and rejects unknown model names.
- Documentation records the asset sources, network requirements, known limitations, and checks run.

## Run locally

Use Python 3.9 or newer from the overlay root. For AI chat, configure a real provider API key on the server—not in browser JavaScript—and run:

```sh
export OPENAI_API_KEY='your-key'
python -m software.web_server
```

Open `http://127.0.0.1:8765`. Without a valid AI API key, the 3D viewer can still operate, while chat correctly reports that no real AI provider is configured. The first 3D-model request downloads about 19–21 MB from the model host for the selected character and caches it. The server must have outbound HTTPS access to `www.innerscene.com`; the browser must have access to Google's hosted `<model-viewer>` runtime. You may set `ROBOT_MODEL_CACHE_DIR` to a persistent storage path.

Run all included tests from the overlay root:

```sh
python -m unittest discover -s tests -v
```

## Current limits and safety

- The 3D models are licensed CC0 rigged human base models. They are **not exact 3D likenesses** reconstructed from the Nova Beige Beulah and Prudence product images.
- Rendering the remote GLB files could not be verified in this build container because outbound DNS/network access is restricted. Automated route, cache, syntax and unit tests pass; a live model load must be verified where outbound HTTPS is available.
- The AI provider is configured separately. No fake replies are used when the provider is unavailable.
- Physical robot movement remains disabled.
- This package has not been pushed to GitHub or deployed to Render.
