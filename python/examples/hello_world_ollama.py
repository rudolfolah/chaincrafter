import argparse
from contextlib import ExitStack
import json
import logging
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import URLError
from urllib.request import urlopen

from chaincrafter import Chain, Prompt
from chaincrafter.models import OpenAiChat


class TimedChat(OpenAiChat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requests = []

    def complete(self, messages):
        started = time.perf_counter()
        before = dict(self.usage)
        record = {"prompt": messages[-1]["content"]}
        self.requests.append(record)
        try:
            record["response"] = super().complete(messages)
            return record["response"]
        except Exception as error:
            record["error"] = str(error)
            raise
        finally:
            record["seconds"] = time.perf_counter() - started
            record["usage"] = {key: value - before[key] for key, value in self.usage.items()}
            logging.info("Request %d completed in %.3fs; usage=%s",
                         len(self.requests), record["seconds"], record["usage"])


def configure_logging(directory):
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    for filename, stream, minimum, maximum in [
        ("stdout.log", sys.stdout, logging.INFO, logging.WARNING),
        ("stderr.log", sys.stderr, logging.WARNING, logging.CRITICAL + 1),
    ]:
        for handler in [logging.StreamHandler(stream),
                        logging.FileHandler(directory / filename, encoding="utf-8")]:
            handler.setLevel(minimum)
            handler.addFilter(lambda record, ceiling=maximum: record.levelno < ceiling)
            handler.setFormatter(formatter)
            root.addHandler(handler)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def stop_server(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def start_server(stack, directory, port):
    # Refuse occupied ports: never silently capture logs from the wrong server.
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", port))
    stdout = stack.enter_context(open(directory / "ollama.stdout.log", "wb"))
    stderr = stack.enter_context(open(directory / "ollama.stderr.log", "wb"))
    process = subprocess.Popen(
        ["ollama", "serve"], stdout=stdout, stderr=stderr,
        env=dict(os.environ, OLLAMA_HOST="127.0.0.1:{}".format(port), OLLAMA_NO_CLOUD="1"),
    )
    stack.callback(stop_server, process)
    deadline = time.perf_counter() + 30
    while time.perf_counter() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Ollama exited; inspect ollama.stderr.log")
        try:
            with urlopen("http://127.0.0.1:{}/api/version".format(port), timeout=1):
                return
        except (URLError, TimeoutError):
            time.sleep(0.1)
    raise TimeoutError("Ollama did not become ready within 30 seconds")


def main():
    parser = argparse.ArgumentParser(description="Run a timed local chain with Ollama and Qwen 0.5B.")
    parser.add_argument("--stream", action="store_true", help="Use streaming HTTP responses")
    parser.add_argument("--log-dir", type=Path, help="Parent for a unique run directory (default: system temp)")
    parser.add_argument("--start-server", action="store_true", help="Start/stop Ollama and capture server stdout/stderr")
    parser.add_argument("--port", type=int, default=11434, help="Local Ollama port (default: 11434)")
    args = parser.parse_args()
    if args.log_dir:
        args.log_dir.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="chaincrafter-ollama-", dir=args.log_dir))
    configure_logging(directory)
    logging.info("Run artifacts: %s", directory)
    # Never send this example to a remotely configured OpenAI endpoint.
    os.environ["OPENAI_BASE_URL"] = "http://127.0.0.1:{}/v1".format(args.port)
    os.environ["OPENAI_API_KEY"] = "ollama"
    report = {"model": "qwen2.5:0.5b", "stream": args.stream,
              "base_url": os.environ["OPENAI_BASE_URL"], "managed_server": args.start_server}
    started = time.perf_counter()
    model = None
    try:
        with ExitStack() as stack:
            if args.start_server:
                server_started = time.perf_counter()
                start_server(stack, directory, args.port)
                report["server_start_seconds"] = time.perf_counter() - server_started
            else:
                logging.info("Using existing server; its process stdout/stderr cannot be captured via the API")
            model = TimedChat(temperature=0.0, model_name=report["model"],
                              max_tokens=32, stream=args.stream)
            stack.callback(model._client.close)
            chain = Chain(
                Prompt("Answer arithmetic questions with only the number, no explanation."),
                (Prompt("What is two plus two?"), "answer"),
                (Prompt("What is {answer} plus three?"), "followup_answer"),
            )
            chain_started = time.perf_counter()
            try:
                report["messages"] = chain.run(model)
            finally:
                report["chain_seconds"] = time.perf_counter() - chain_started
            for message in report["messages"]:
                logging.info("%s: %s", message["role"], message["content"])
            report["status"] = "ok"
    except Exception as error:
        report.update(status="error", error=str(error))
        logging.exception("Ollama example failed")
    finally:
        report["total_seconds"] = time.perf_counter() - started
        if model is not None:
            report.update(requests=model.requests, usage=model.usage)
        (directory / "result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        logging.info("Total %.3fs; chain %s seconds; usage=%s; status=%s",
                     report["total_seconds"], report.get("chain_seconds"),
                     report.get("usage"), report["status"])
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
