"""Tests for the allowlisted, same-origin GLB cache/proxy route."""
from __future__ import annotations

import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.request import urlopen

from software import web_server


class DummyService:
    def status(self):
        return {"ai_configured": False, "model": "", "conversation_messages": 0}

    def history(self):
        return []


class ModelRouteTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_patch = patch.object(web_server, "MODEL_CACHE_DIR", Path(self.temp_dir.name))
        self.cache_patch.start()
        self.blob = b"glTF" + b"\x02\x00\x00\x00" + b"\x0c\x00\x00\x00"
        self.upstream = patch.object(web_server, "urlopen", return_value=FakeResponse(self.blob))
        self.urlopen_mock = self.upstream.start()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), web_server.make_handler(DummyService(), ""))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = "http://127.0.0.1:%d" % self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.upstream.stop()
        self.cache_patch.stop()
        self.temp_dir.cleanup()

    def test_allowlisted_model_is_served_as_same_origin_glb_and_cached(self):
        with urlopen(self.base + "/api/3d-models/beulah.glb", timeout=3) as response:
            first = response.read()
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), "model/gltf-binary")
        with urlopen(self.base + "/api/3d-models/beulah.glb", timeout=3) as response:
            second = response.read()
        self.assertEqual(first, self.blob)
        self.assertEqual(second, self.blob)
        self.urlopen_mock.assert_called_once()

    def test_unknown_model_name_is_not_proxied(self):
        try:
            urlopen(self.base + "/api/3d-models/other.glb", timeout=3)
        except Exception as exc:
            self.assertIn("404", str(exc))
        else:
            self.fail("unknown model route should return 404")
        self.urlopen_mock.assert_not_called()


class FakeResponse:
    def __init__(self, body: bytes):
        self.body = body
        self.read_count = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, limit: int):
        self.read_count += 1
        return self.body[:limit]


if __name__ == "__main__":
    unittest.main()
