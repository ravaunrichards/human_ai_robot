# Render service map — human_ai_robot

| Resource | Blueprint action | Reason |
|---|---|---|
| `human-ai-robot-virtual-ai` (existing web service) | Adopt/maintain existing resource | Serves the UI and `/api/*` routes from one Python process. |
| PostgreSQL database | Not defined | Current virtual AI stores recent conversation history in process memory; no database integration is wired into this service. |
| Redis / Key Value | Not defined | No Redis client or queue integration is implemented in this app package. |
| Background worker | Not defined | No independent worker entrypoint is present in this implementation. |
| Static-site service | Not defined | The Python web service serves `web/` assets and API endpoints from one origin. Splitting it would require app/CORS/auth changes, so this Blueprint does not invent a second frontend. |

## Existing service snapshot

Render returned the existing service as `not_suspended` with a live deployment. The latest listed deploy had status `live`, and the corresponding build and deploy events were `succeeded`. This checks Render's recorded state; it is not an independent browser test of every app endpoint or proof that AI credentials and external 3D model downloads work.
