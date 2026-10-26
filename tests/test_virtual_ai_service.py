"""Safety and behaviour tests for the live browser AI service."""
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from software.virtual_ai_service import AINotConfigured, AIProviderFailure, VirtualAIService


class VirtualAIServiceTests(unittest.TestCase):
    def test_missing_key_fails_explicitly_without_creating_fake_reply(self):
        service = VirtualAIService(api_key="", request_fn=None)
        self.assertFalse(service.status()["ai_configured"])
        with self.assertRaises(AINotConfigured):
            service.reply("Hello")
        self.assertEqual(service.history(), [])

    def test_real_provider_reply_is_shared_in_history(self):
        def real_provider_for_test(messages):
            self.assertEqual(messages[-1].role, "user")
            return "Test-provider response used by this unit test."

        service = VirtualAIService(api_key="unit-test-key", request_fn=real_provider_for_test)
        answer = service.reply("Hello from the test")
        self.assertEqual(answer, "Test-provider response used by this unit test.")
        history = service.history()
        self.assertEqual([item["role"] for item in history], ["user", "assistant"])
        self.assertEqual(history[0]["content"], "Hello from the test")
        self.assertEqual(history[1]["content"], answer)
        self.assertTrue(service.status()["ai_configured"])
        self.assertTrue(service.status()["simulation_only"])
        self.assertEqual(service.status()["motion_control"], "disabled")
        self.assertFalse(service.status()["reply_fallback"])

    def test_provider_failure_is_not_replaced_by_echo(self):
        def failing_provider(_messages):
            raise RuntimeError("provider unavailable")

        service = VirtualAIService(api_key="unit-test-key", request_fn=failing_provider)
        with self.assertRaises(AIProviderFailure):
            service.reply("Do not fabricate a reply")
        self.assertEqual(service.history(), [])

    def test_empty_and_oversized_messages_are_rejected(self):
        service = VirtualAIService(api_key="unit-test-key", request_fn=lambda _messages: "ok")
        with self.assertRaises(ValueError):
            service.reply("   ")
        with self.assertRaises(ValueError):
            service.reply("x" * 4001)
        self.assertEqual(service.history(), [])


    def test_openai_compatible_http_request_uses_server_key_and_parses_real_response_shape(self):
        captured = {}

        class ProviderHandler(BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802
                captured["path"] = self.path
                captured["authorization"] = self.headers.get("Authorization")
                length = int(self.headers.get("Content-Length", "0"))
                captured["payload"] = json.loads(self.rfile.read(length).decode("utf-8"))
                body = json.dumps({"choices": [{"message": {"role": "assistant", "content": "Response from the test HTTP provider."}}]}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, _fmt, *_args):
                return

        server = HTTPServer(("127.0.0.1", 0), ProviderHandler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            service = VirtualAIService(
                api_key="unit-test-secret",
                model="unit-test-model",
                base_url="http://127.0.0.1:%s/v1" % server.server_port,
            )
            answer = service.reply("Hello from the browser")
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=2)

        self.assertEqual(answer, "Response from the test HTTP provider.")
        self.assertEqual(captured["path"], "/v1/chat/completions")
        self.assertEqual(captured["authorization"], "Bearer unit-test-secret")
        self.assertEqual(captured["payload"]["model"], "unit-test-model")
        self.assertEqual(captured["payload"]["messages"][-1], {"role": "user", "content": "Hello from the browser"})
        self.assertNotIn("unit-test-secret", json.dumps(captured["payload"]))

    def test_reset_clears_shared_conversation_but_preserves_system_instruction(self):
        service = VirtualAIService(api_key="unit-test-key", request_fn=lambda _messages: "ok")
        service.reply("hello")
        service.clear_history()
        self.assertEqual(service.history(), [])
        self.assertTrue(service.status()["ai_configured"])
        self.assertEqual(service.reply("after reset"), "ok")
        self.assertEqual(service.history()[0]["content"], "after reset")


if __name__ == "__main__":
    unittest.main()
