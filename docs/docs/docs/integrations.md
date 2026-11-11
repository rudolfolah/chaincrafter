Integrations available

| Integration | Status, Python | Status, JavaScript |
| ----------- | -------------- |--------------------|
| OpenAI: GPT-3.5, GPT-4 | Stable | In development |
| Ollama via OpenAI-compatible API | Local example verified | Not integrated |
| Llama.cpp | In development | In development |

Install the OpenAI integration with `pip install 'chaincrafter[openai]'` and set
`OPENAI_API_KEY`. It uses the SDK's `OpenAI` client and Chat Completions API.
Installation selects OpenAI SDK 2.2.x on Python 3.8, 2.48.0+ on Python 3.9,
or 3.48.0+ on Python 3.10 and newer. Later SDK releases require dependencies
that no longer support Python 3.8.

With `stream=True`, `OpenAiChat.complete()` consumes the stream and returns the
complete first-choice text, so it works with `Chain.run()` and `Chain.async_run()`.
Reported streaming token usage is added to the model's cumulative totals; if the
server omits usage, those totals remain unchanged.

The experimental `LlamaCppChat` uses `LLAMA_CPP_PATH` as the executable path and
the supplied `model_name` as the model file path. The integration remains in
development.

## Local Ollama

Use the existing `OpenAiChat` adapter with Ollama's
[OpenAI-compatible API](https://docs.ollama.com/api/openai-compatibility).
The example uses [`qwen2.5:0.5b`](https://ollama.com/library/qwen2.5:0.5b),
a small model with a roughly 397 MB download. It is suitable for local integration
checks, not a substitute for larger models on complex tasks.

On macOS, install Ollama and start a localhost-only server in a separate terminal:

```bash
brew install ollama
OLLAMA_HOST=127.0.0.1:11434 OLLAMA_NO_CLOUD=1 ollama serve
```

Leave that terminal running; Ctrl-C stops the server. If Ollama is already running
on port 11434, reuse it rather than starting another server. Download the model:

```bash
OLLAMA_HOST=127.0.0.1:11434 ollama pull qwen2.5:0.5b
```

From the repository root, run the example using `uv` and Python 3.11:

```bash
cd python
PYTHONPATH=. uv run --no-project --python 3.11 --with pyyaml --with openai \
  python examples/hello_world_ollama.py
PYTHONPATH=. uv run --no-project --python 3.11 --with pyyaml --with openai \
  python examples/hello_world_ollama.py --stream
```

The example sets `OPENAI_BASE_URL=http://127.0.0.1:11434/v1` and
`OPENAI_API_KEY=ollama` within its own process, overriding any remote OpenAI
configuration. The key is a nonsecret SDK requirement; local Ollama ignores it.
Model downloads require network access, but these completions run locally.

Both modes execute a two-step chain, passing the first answer into the second
prompt. INFO logs go to stdout; warnings, errors, and failure tracebacks go to
stderr. Each run creates a unique directory (printed at startup) containing:

* `stdout.log` and `stderr.log`: copies of the example's console logs.
* `result.json`: collected model responses, complete messages on success,
  per-request elapsed seconds and token usage, cumulative usage, chain elapsed
  seconds, total elapsed seconds, and success/error status. Failed requests retain
  their timing and error. Timing uses a monotonic performance counter.

Choose an artifact parent with `--log-dir /tmp/chaincrafter-runs`; otherwise the
system temporary directory is used. Logs contain prompts and responses; treat
them as potentially sensitive. Temporary directories may be cleared by the OS.
Request times include HTTP and inference time; the first request may also include
model loading. These are client wall-clock timings, not Ollama inference-only
metrics. Total time includes client setup and managed-server startup/shutdown,
but not Python interpreter startup. Streaming is consumed internally;
`Chain.run()` returns complete messages, not live token output.

To collect Ollama's process output too, let the example start its own server on
an unused port. The model must already be downloaded:

```bash
PYTHONPATH=. uv run --no-project --python 3.11 --with pyyaml --with openai \
  python examples/hello_world_ollama.py --stream --start-server --port 11435 \
  --log-dir /tmp/chaincrafter-runs
```

This adds `ollama.stdout.log`, `ollama.stderr.log`, and server-start elapsed
seconds. The server is localhost-only with cloud disabled and is stopped when
the example exits, including on errors. Occupied ports are rejected rather than
silently reusing a server. Without `--start-server`, model replies are collected
but an existing server's stdout/stderr cannot be retrieved through the API.
Failures produce an error report and a nonzero exit code.

Verified locally with Ollama 0.40.15: answers `4` and `7` in both modes.
The timed example was also checked with a managed server on port 11435, including
captured server logs, shutdown, and an occupied-port failure.
Keep `n=1` and omit `logit_bias`; Ollama does not support those OpenAI options.
