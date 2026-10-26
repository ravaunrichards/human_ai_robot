# Run the human_ai_robot virtual AI in a browser

This adds a mobile-friendly browser interface to the existing repository. It reuses `software.conversation.OnlineProvider` and `Message`, but intentionally does **not** use the legacy echo fallback for browser conversations. If the real model is not configured or the provider fails, the UI shows an error instead of inventing an AI reply.

## 1. Requirements

- Python 3.9 or newer.
- A valid OpenAI API key with API access and available billing/credits. ChatGPT subscriptions and API usage are separate; do not put the key in frontend JavaScript or commit it to Git.
- Internet access from the server to the AI API.

## 2. Start the server

From the repository root:

**Linux / macOS**

```sh
export OPENAI_API_KEY='paste-your-key-here'
export OPENAI_MODEL='gpt-5.5'  # optional; use a model enabled for your API account
python -m software.web_server
```

**Windows PowerShell**

```powershell
$env:OPENAI_API_KEY = 'paste-your-key-here'
$env:OPENAI_MODEL = 'gpt-5.5'  # optional; use a model enabled for your API account
python -m software.web_server
```

Then open `http://127.0.0.1:8765` on the computer running the server. The API key is read server-side only. The default server uses the standard-library HTTP server and does not require FastAPI or another framework.

The server calls the OpenAI-compatible Chat Completions API using the official `/v1/chat/completions` endpoint shape. `OPENAI_BASE_URL` can change the API base for an OpenAI-compatible provider. If the account does not have access to the configured model, change `OPENAI_MODEL` to a model available to that account.

## 3. Use it from phone and computer on one Wi-Fi network

Run the server on a trusted computer. Set an access token before allowing other devices to connect:

**Linux / macOS**

```sh
export ROBOT_ACCESS_TOKEN='use-a-long-unique-random-secret'
python -m software.web_server --host 0.0.0.0 --port 8765
```

**Windows PowerShell**

```powershell
$env:ROBOT_ACCESS_TOKEN = 'use-a-long-unique-random-secret'
python -m software.web_server --host 0.0.0.0 --port 8765
```

Find the computer's private LAN IP address (for example, `192.168.1.20`) and open `http://192.168.1.20:8765` on the phone. Replace the example address with the computer's actual address. Enter the same `ROBOT_ACCESS_TOKEN` on both devices. The server owns one shared in-memory conversation; messages from either device appear in both interfaces within a few seconds.

The access token protects the chat, history, and reset endpoints. The service refuses to bind to a non-loopback address without this token. Use only on a trusted LAN. For access across the internet, deploy behind a properly configured HTTPS reverse proxy or authenticated hosting platform; do not expose the raw HTTP server directly to the public internet.

## Configuration variables

| Variable | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | none | Server-side API credential. Without it, chat is disabled and no fake reply is produced. |
| `OPENAI_MODEL` | `gpt-5.5` | Model identifier enabled for the API account. |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API base URL; supports compatible endpoints. |
| `ROBOT_AI_SYSTEM_PROMPT` | built-in robotics-safe prompt | Optional replacement instruction for the conversational model. |
| `ROBOT_HOST` | `127.0.0.1` | Listener address; non-loopback binding requires an access token. |
| `ROBOT_PORT` | `8765` | Listener port. |
| `ROBOT_ACCESS_TOKEN` | none | Required for non-loopback hosting; same secret must be entered on every device. |


## Deploy for access beyond your Wi-Fi

The same app can run on one hosted Python web service and serve both the phone and computer. On a platform such as Render, connect the repository **after adding these new files**, set the build command to `pip install -e .`, and the start command to `python -m software.web_server --host 0.0.0.0`. Configure `OPENAI_API_KEY`, `ROBOT_ACCESS_TOKEN`, and optionally `OPENAI_MODEL` as protected environment variables in the hosting dashboard—not in source code. The server reads the platform's `PORT` variable automatically. Use the platform's HTTPS URL, enter the same access token on both devices, and keep a single server instance because this first version shares conversation state in process memory. Choose an always-on plan if you need consistent availability; a platform that sleeps or restarts may interrupt the session and clear history.

## Honest current limits

- This is a real model-backed chat UI only after the server is configured with a valid API key and an accessible model. The status endpoint reports configuration; a successful first response verifies the provider credentials/model.
- The avatar is an interface illustration, not a rendered 3D body, webcam feed, or robot hardware.
- History is shared in server memory while the server runs, but is not persisted across server restarts.
- Voice input uses the browser's built-in speech recognition when available. Spoken AI output uses the device's speech synthesis. Browser support and microphone permission vary by device.
- The web UI does not send motion commands. Physical movement remains disabled and must continue to be controlled by the repository's independent safety gate and real-time layer.
- The Python server is a single-owner starting point, not an internet-hardened multi-user service. Use HTTPS, strong access control, rate limits, and managed secrets before public deployment.

## Tests

The added unit tests cover unconfigured-provider behaviour, real-provider adapter integration via a test double, non-fallback on provider failure, input limits, and shared-session reset:

```sh
python -m unittest tests.test_virtual_ai_service -v
```

These tests do not make real paid API calls. A live API check should be done manually after setting `OPENAI_API_KEY`.
