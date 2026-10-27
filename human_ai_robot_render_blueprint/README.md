# human_ai_robot — Render Blueprint package

This package defines the Render Blueprint for the existing service `human-ai-robot-virtual-ai` in `ravaunrichards/human_ai_robot`.

## Existing resource inspected

- Service: `human-ai-robot-virtual-ai`
- Service ID: `srv-dbfie3q9lscs73a94rc0`
- Repository: `https://github.com/ravaunrichards/human_ai_robot`
- Branch: `main`
- Public URL: `https://human-ai-robot-virtual-ai.onrender.com`
- Runtime: Python
- Region: Virginia
- Current build command: `pip install -e .`
- Current start command: `python -m software.web_server --host 0.0.0.0`
- Render's latest recorded deployment at inspection time: `live`; its build and deploy events reported success.

The Blueprint intentionally uses the **same service name** so it targets the existing service. It is not intended to create a duplicate service. During Blueprint setup, inspect Render's proposed changes: if it proposes creating a second `human-ai-robot-virtual-ai` service, cancel rather than continuing.

## Included resources

Only one Render service is defined. The current application is a single Python web process that serves the browser UI and its API routes. No separate database, queue, or background worker is declared because the supplied application does not currently implement those separate services. Its conversation history is in memory and does not persist through process restarts.

## Blueprint changes represented

- Preserve the existing repository, branch, runtime, plan, region, build command, and start command.
- Add `/api/health` as Render's process health-check route.
- Preserve commit-based automatic deploy behavior already configured on the existing service.
- Prompt for `OPENAI_API_KEY` if it is not already configured when initially adding it to the Blueprint.
- Ensure `ROBOT_ACCESS_TOKEN` exists for safe non-loopback binding; Render generates it only if the variable does not already exist.

No API key or other secret is included in this package.

## How to apply safely

1. Download and extract this package.
2. Place `render.yaml` at the **root** of `ravaunrichards/human_ai_robot` on branch `main`. The app files must remain at repository root, including `software/` and the package metadata used by `pip install -e .`.
3. In Render, create/sync a Blueprint for that repository and review the proposed resource changes carefully.
4. Confirm the Blueprint references/adopts the existing `human-ai-robot-virtual-ai` service. If it proposes a new duplicate, stop.
5. Sync the Blueprint, then verify the service is healthy at `https://human-ai-robot-virtual-ai.onrender.com/api/health` and inspect Render deploy events.

The existing service currently has commit auto-deploy enabled. Adding `render.yaml` as a new commit can therefore trigger the existing service's regular auto-deploy even before Blueprint sync. Do not make the commit until you are ready for that deploy.

## Safety and scope

- Creating this package did not modify GitHub or Render.
- It does not create, resume, or recreate any deleted/suspended services.
- It does not add a database, queue, worker, or paid persistent disk.
- `OPENAI_API_KEY` must be a valid API key with billing/credits and access to the configured model; the Blueprint cannot create API credits.
- `ROBOT_ACCESS_TOKEN` is a server access credential. Do not commit its actual value or share it publicly.
- The app remains simulation-only; physical robot motor control is not enabled by this Blueprint.
