"""Validate the local Render Blueprint YAML without contacting Render."""
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required only to run this local validation: python -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)

path = Path(__file__).with_name("render.yaml")
data = yaml.safe_load(path.read_text(encoding="utf-8"))
services = data.get("services")
assert isinstance(services, list) and len(services) == 1, "Expected exactly one implemented service; do not create placeholder services."
svc = services[0]
assert svc.get("type") == "web", "Expected a Render web service."
assert svc.get("name") == "human-ai-robot-virtual-ai", "Service name must match the existing service to avoid duplicates."
assert svc.get("repo") == "https://github.com/ravaunrichards/human_ai_robot", "Unexpected repository target."
assert svc.get("branch") == "main", "Expected existing main branch."
assert svc.get("buildCommand") == "pip install -e .", "Build command must match the existing service."
assert svc.get("startCommand") == "python -m software.web_server --host 0.0.0.0", "Start command must match the existing service."
assert svc.get("healthCheckPath") == "/api/health", "Health check should use implemented route."
assert svc.get("region") == "virginia" and svc.get("plan") == "free", "Region/plan must match existing service."
assert svc.get("autoDeployTrigger") == "commit", "Automatic deploy behavior should match existing service."
env = {item.get("key"): item for item in svc.get("envVars", [])}
assert env.get("OPENAI_API_KEY", {}).get("sync") is False, "Do not hardcode API secrets."
assert env.get("ROBOT_ACCESS_TOKEN", {}).get("generateValue") is True, "Ensure remote listener has a protected access token."
raw = path.read_text(encoding="utf-8")
assert not re.search(r"(?:sk-[A-Za-z0-9_-]{20,}|OPENAI_API_KEY\s*:\s*['\"]?sk-)", raw), "Possible embedded API key found."
print("PASS: render.yaml parses as YAML")
print("PASS: exactly one implemented Render service is defined")
print("PASS: target name/repository/branch match inspected existing service")
print("PASS: build/start commands, plan, region, and auto-deploy behavior match existing service")
print("PASS: health check points to /api/health")
print("PASS: API secret is not hardcoded and access-token generation is declared")
print("PASS: no placeholder database/worker/static services are defined")
