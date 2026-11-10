Integrations available

| Integration | Status, Python | Status, JavaScript |
| ----------- | -------------- |--------------------|
| OpenAI: GPT-3.5, GPT-4 | Stable | In development |
| Llama.cpp | In development | In development |

Install the OpenAI integration with `pip install 'chaincrafter[openai]'` and set
`OPENAI_API_KEY`. It uses the SDK's `OpenAI` client and Chat Completions API.
Installation selects OpenAI SDK 2.2.x on Python 3.8, 2.48.0+ on Python 3.9,
or 3.48.0+ on Python 3.10 and newer. Later SDK releases require dependencies
that no longer support Python 3.8.
