# chaincrafter

Seamless integration and composability for large language model apps.

## Features
* Composable prompts and chains
  * Use multiple models to run one chain and then use that as input for a different chain and model
* Customizable prompt and response formatting
  * Add modifiers to prompts to change the style, length, and format of the response
  * Extract data from the response to use in the next prompt
  * Add custom functions to process the response
  * Add custom functions to process the input variables
* Integration with OpenAI API (llama.cpp in progress)
* Async calls to models
* Load Prompts and Chains from YAML using Catalogs
  * Makes it easier to share prompts and chains between projects
  * Build up a prompts library

## Installation
```bash
pip install chaincrafter
```

## Usage

1. Define your prompts and the variables that they expect
  - The input variables can be of any type, and can be processed by a function
  - The prompt message is treated as an _f-string_
2. Define your chain of prompts
  - The chain is a list of tuples, where each tuple contains a prompt and the output key to store the response in
  - The output key is used to access the response in the next prompt
3. Set up the models that you want to use
4. Run the chain using the models

```python
from chaincrafter import Chain, Prompt
from chaincrafter.models import OpenAiChat

chat_model = OpenAiChat(temperature=0.65, model_name="gpt-3.5-turbo")
system_prompt = Prompt("You are a helpful assistant who responds to questions about the world")
hello_prompt = Prompt("Hello, what is the capital of France? Answer only with the city name.")
followup_prompt = Prompt("{city} sounds like a nice place to visit. What is the population of {city}?")
chain = Chain(
    system_prompt,
    (hello_prompt, "city"),
    (followup_prompt, "followup_response"),
)
messages = chain.run(chat_model)
for message in messages:
    print(f"{message['role']}: {message['content']}")
```

### Running the examples
```bash
source venv/bin/activate
export OPENAI_API_KEY="..."
python -m examples.interesting_facts
python -m examples.interesting_facts_catalog
```