# Apply this virtual AI web update to the existing repository

This is an **additions-only overlay** for `ravaunrichards/human_ai_robot`. The following paths were checked on 2026-10-26 and did not exist in the repository, so the overlay will not replace existing source files:

- `software/virtual_ai_service.py`
- `software/web_server.py`
- `web/index.html`
- `web/app.css`
- `web/app.js`
- `tests/test_virtual_ai_service.py`
- `docs/virtual_ai_web.md`

## Apply

Extract this ZIP into the root of a fresh checkout of `https://github.com/ravaunrichards/human_ai_robot`. Keep the directory structure shown above. Do not copy any API key into these files.

## Run locally

From the repository root, configure a real API key on the computer/server (not in the browser):

**Linux/macOS:** `export OPENAI_API_KEY='your-key'`

**Windows PowerShell:** `$env:OPENAI_API_KEY = 'your-key'`

Then run `python -m software.web_server` and open `http://127.0.0.1:8765`. See `docs/virtual_ai_web.md` for LAN sharing, a shared access token, and hosted deployment guidance.

To share one conversation on a phone and computer on the same Wi-Fi network, set `ROBOT_ACCESS_TOKEN` and run `python -m software.web_server --host 0.0.0.0`. Open the computer's LAN IP and port 8765 on the phone, then enter the same access token on both devices. Never expose this raw server directly to the public internet; use a hosted HTTPS service and protected environment variables for remote access.

Run the added unit tests with `python -m unittest discover -s tests -p 'test_virtual_ai_service.py' -v`.

## Safety and limits

- No OpenAI API key is bundled.
- No fake/echo response is used for browser chat. Without a real model credential, chat is blocked with a clear setup message.
- The avatar is an interface illustration, not a physical robot or an asserted 3D simulation.
- Real hardware motion remains disabled.
- Shared conversation history is held in server memory and clears when the server restarts.
