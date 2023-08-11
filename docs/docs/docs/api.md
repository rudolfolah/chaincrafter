# Python

## `chaincrafter.catalogs`
A catalog is a collection of chains and prompts stored in a YAML file.

- `Catalog`
    - `load(path: str)`
    - `get_chain(chain_id: str) -> Chain`
    - `get_prompt(prompt_id: str, prompt_modifiers: [Callable] = [], **input_vars_transformers: [dict[str, Callable]]) -> Prompt`
    - `__getitem__(prompt_id: str) -> Prompt`

## `chaincrafter.chains`
- `Chain`
    - `run(chat_model: ChatModel, starting_input_vars: dict) -> [Message]`: Runs the chain given a `ChatModel` and a set of starting input variables. 
    - `async_run(chat_model: ChatModel, starting_input_vars: dict) -> [Message]`: Runs the chain asynchronously using `asyncio`, see [Async](./async.md)
- `Message`, a typed dictionary (based on the response from OpenAI API)

## `chaincrafter.experiments`
- `Experiment`
    - `Experiment(chain: Chain, **model_params)`
    - `set_chain_starting_input_vars(starting_input_vars: dict)`
    - `prepare()`
    - `run(runs: int = 1)`
    - `to_csv()`
    - `to_pandas_df()`
    - `to_json()`
    - `visualize()`
- `OpenAiChatExperiment(Experiment)` 

## `chaincrafter.models`
- `ChatModel`
    - `ChatModel(temperature: float, model_name: str)`
    - `complete(messages: [dict]) -> str`
    - `show_usage()`
- `MockChat(ChatModel)`
    - `MockChat(temperature: float, model_name: str)`
    - `mock_responses(messages: [dict])`
    - `complete(messages: [dict])`
- `OpenAiChat(ChatModel)`
    - `OpenAiChat(temperature: float, model_name: str, top_p: float, n: int, stream: bool, stop: [str], max_tokens: int, presence_penalty: float, frequency_penalty: float, logit_bias: dict)`: same API as [OpenAI API](https://platform.openai.com/docs/api-reference/chat/create)
    - `complete(messages: [dict])`
    - `show_usage()`

## `chaincrafter.prompts`
- `Prompt`
    - `Prompt(fmt_str: str, prompt_modifiers: [Callable], **input_vars_transformers: [dict[str, Callable]])`
    - `build(**input_vars: dict) -> str`
- `response_format_list(example_item_text: str) -> Callable[[str], str]`
- `response_style(style_of: str) -> str`
- `response_length(short_or_long: str = "short", answer_or_paragraph: str = "sentence") -> str`
- `extract_items_from_list(response: str) -> [str]`

# JavaScript/TypeScript

*work in progress*

# Catalog Format YAML
YAML file format for Catalogs:

```yaml
prompts:
  helpful_assistant: You are a helpful assistant
  initial_code_review: |
    I just put a lot of work into this code, can you please review it and offer suggestions for improvement? Do not write any code.
    ```
    {diff}
    ```
  city_population: "{city} sounds like a nice place to visit. What is the population of {city}?"
chains:
  example:
    - helpful_assistant:
    - initial_code_review: city
    - city_population: output
``` 
