# Examples

For a local, API-key-free example, see `hello_world_ollama.py` and the
[Ollama setup instructions](../../docs/docs/docs/integrations.md#local-ollama).
It uses the 397 MB `qwen2.5:0.5b` model; add `--stream` to exercise streaming.
Use `--log-dir /tmp/chaincrafter-runs` to save timed responses and split
stdout/stderr logs. Add `--start-server --port 11435` to capture Ollama server
output as well; the example stops that server afterward.

Some of the examples are based on the examples from the following libraries:
* [MiniChain](https://github.com/srush/MiniChain)
* [LangChain](https://python.langchain.com/docs/use_cases)
