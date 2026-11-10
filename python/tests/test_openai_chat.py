import importlib.util
import json
import os
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

from chaincrafter import Chain, Prompt
from chaincrafter.models import OpenAiChat


@unittest.skipUnless(importlib.util.find_spec("openai"), "requires the openai extra")
class TestOpenAiChat(unittest.TestCase):
    def test_chained_responses_and_cumulative_usage(self):
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                question = request["messages"][-1]["content"]
                answers = {"Capital of France?": "Paris", "Population of Paris?": "2 million"}
                if question not in answers:
                    self.send_error(400, "Unexpected chain input")
                    return
                response = json.dumps({
                    "id": "chatcmpl-test",
                    "object": "chat.completion",
                    "created": 0,
                    "model": "test-model",
                    "choices": [{
                        "index": 0,
                        "message": {"role": "assistant", "content": answers[question]},
                        "finish_reason": "stop",
                    }],
                    "usage": {"prompt_tokens": 10, "completion_tokens": 3, "total_tokens": 13},
                }).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)

            def log_message(self, format, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.addCleanup(server.server_close)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join)
        self.addCleanup(server.shutdown)
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-key",
            "OPENAI_BASE_URL": "http://127.0.0.1:{}/v1".format(server.server_port),
        }, clear=True):
            model = OpenAiChat(0.7, "test-model")
        self.addCleanup(model._client.close)
        chain = Chain(
            Prompt("Answer briefly"),
            (Prompt("Capital of France?"), "city"),
            (Prompt("Population of {city}?"), "population"),
        )
        messages = chain.run(model)
        self.assertEqual([m["content"] for m in messages if m["role"] == "assistant"],
                         ["Paris", "2 million"])
        self.assertEqual(model.usage, {"prompt_tokens": 20, "completion_tokens": 6, "total_tokens": 26})
