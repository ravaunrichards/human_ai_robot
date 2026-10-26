"""Small dependency-free HTTP server for the synchronised virtual AI UI.

Run with: python -m software.web_server
The listener defaults to loopback. Binding to a non-loopback address requires
ROBOT_ACCESS_TOKEN so an accidentally exposed deployment cannot spend API
credits or expose the shared conversation without a token.
"""
from __future__ import annotations

import argparse
import hmac
import ipaddress
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse

from software.virtual_ai_service import AINotConfigured, AIProviderFailure, VirtualAIService


ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = ROOT / "web"
MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
}
MAX_REQUEST_BYTES = 16_384


def _is_loopback(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host) in ipaddress.ip_network("127.0.0.0/8") or ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def make_handler(service: VirtualAIService, access_token: str):
    class VirtualAIHandler(BaseHTTPRequestHandler):
        server_version = "human-ai-robot/1.0"

        def log_message(self, fmt: str, *args) -> None:
            # Do not log request bodies, auth headers, or conversation contents.
            super().log_message(fmt, *args)

        def _headers(self, content_type: str, length: int) -> None:
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(length))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")

        def _send_json(self, status: int, payload: Dict[str, object]) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self._headers("application/json; charset=utf-8", len(body))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _authorised(self) -> bool:
            if not access_token:
                return True
            supplied = self.headers.get("Authorization", "")
            if supplied.lower().startswith("bearer "):
                supplied = supplied[7:].strip()
            else:
                supplied = self.headers.get("X-Robot-Access-Token", "")
            return hmac.compare_digest(supplied, access_token)

        def _require_auth(self) -> bool:
            if self._authorised():
                return True
            self._send_json(401, {"error": "Access key required or invalid.", "requires_access_token": True})
            return False

        def _read_json(self) -> Dict[str, object]:
            raw_length = self.headers.get("Content-Length", "0")
            try:
                length = int(raw_length)
            except ValueError as exc:
                raise ValueError("Invalid Content-Length.") from exc
            if length < 0 or length > MAX_REQUEST_BYTES:
                raise ValueError("Request is too large.")
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ValueError("Request must contain valid JSON.") from exc
            if not isinstance(data, dict):
                raise ValueError("Request body must be a JSON object.")
            return data

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path in ("/api/status", "/api/health"):
                payload = service.status()
                payload["requires_access_token"] = bool(access_token)
                payload["message"] = (
                    "Real AI provider configured; first reply still verifies API access."
                    if payload["ai_configured"]
                    else "AI is not configured. Set OPENAI_API_KEY on the server; no sample replies are generated."
                )
                self._send_json(200, payload)
                return
            if path == "/api/history":
                if not self._require_auth():
                    return
                self._send_json(200, {"messages": service.history()})
                return

            relative = "index.html" if path in ("/", "/index.html") else path.lstrip("/")
            candidate = (WEB_ROOT / relative).resolve()
            try:
                candidate.relative_to(WEB_ROOT.resolve())
            except ValueError:
                self._send_json(404, {"error": "Not found."})
                return
            if not candidate.is_file() or candidate.suffix.lower() not in MIME_TYPES:
                self._send_json(404, {"error": "Not found."})
                return
            try:
                body = candidate.read_bytes()
            except OSError:
                self._send_json(500, {"error": "Could not read application asset."})
                return
            self.send_response(200)
            self._headers(MIME_TYPES[candidate.suffix.lower()], len(body))
            self.send_header("Cache-Control", "no-cache" if candidate.name == "index.html" else "public, max-age=300")
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path not in ("/api/chat", "/api/reset"):
                self._send_json(404, {"error": "Not found."})
                return
            if not self._require_auth():
                return
            try:
                data = self._read_json()
                if path == "/api/reset":
                    service.clear_history()
                    self._send_json(200, {"ok": True, "messages": []})
                    return
                message = data.get("message")
                if not isinstance(message, str):
                    raise ValueError("Message must be a string.")
                answer = service.reply(message)
                self._send_json(200, {"reply": answer, "messages": service.history()})
            except ValueError as exc:
                self._send_json(400, {"error": str(exc)})
            except AINotConfigured as exc:
                self._send_json(503, {"error": str(exc), "ai_configured": False})
            except AIProviderFailure as exc:
                self._send_json(502, {"error": str(exc), "ai_configured": True})
            except Exception as exc:  # noqa: BLE001
                # Return a generic error; never expose traceback/config/secrets.
                print("Virtual AI internal error: %s" % exc.__class__.__name__)
                self._send_json(500, {"error": "Unexpected server error. Check server logs."})

    return VirtualAIHandler


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the human_ai_robot synchronised virtual AI web app.")
    parser.add_argument("--host", default=os.environ.get("ROBOT_HOST", "127.0.0.1"), help="Bind address (non-loopback requires ROBOT_ACCESS_TOKEN).")
    parser.add_argument("--port", type=int, default=int(os.environ.get("ROBOT_PORT", os.environ.get("PORT", "8765"))), help="TCP port (default: ROBOT_PORT, platform PORT, or 8765).")
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    access_token = os.environ.get("ROBOT_ACCESS_TOKEN", "").strip()
    if not _is_loopback(args.host) and not access_token:
        parser.error("ROBOT_ACCESS_TOKEN is required when binding to a non-loopback address.")
    if not (WEB_ROOT / "index.html").is_file():
        parser.error("web/index.html is missing; install the complete repository, not just software/.")

    service = VirtualAIService()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(service, access_token))
    print("human_ai_robot virtual AI server")
    print("URL: http://%s:%s" % (args.host, args.port))
    print("AI provider: %s" % (service.model if service.status()["ai_configured"] else "NOT CONFIGURED — set OPENAI_API_KEY"))
    print("Mode: SIMULATION ONLY; real motor control disabled")
    if access_token:
        print("Remote access: access-key protection enabled")
    print("Stop with Ctrl+C.")
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        print("\nStopping virtual AI server...")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
