Experiments are a way to run a set of prompt chains with a variety of model parameters and compare the results. This is useful for finding the best model parameters for a given prompt chain. It is also useful to store and compare the results at later points in time.

# Experiment

An experiment that runs a chat model on a prompt. Generates all permutations of the variables provided.

* `Experiment(message, **model_params)`: Create an experiment with the given prompts chain and the model parameters
* `Experiment.run(runs=1)`: Run the experiment
* `Experiment.model_class`: The model class used in the experiment
* `Experiment.results`: The results of the experiment
* `Experiment.prepare()`: Prepare the experiment by generating the Cartesian product of the model parameters

# OpenAI Chat Experiment

You can set up an experiment with the model parameters for OpenAI Chat like this:

```python
from chaincrafter.experiments import OpenAiChatExperiment
# ...
experiment = OpenAiChatExperiment(
    chain,
    model_name=["gpt-4", "gpt-3.5-turbo"],
    temperature=[0.7, 1.5],
    presence_penalty=[0.1],
    frequency_penalty=[0.2],
    max_tokens=[100, 300, None],
)
```

All of the parameters will be set to defaults if you don't specify them. Specify one value by using a list with one item (e.g. `model_name=["gpt-4"]`).

## Example

### Code

```python
from chaincrafter import Chain, Prompt
from chaincrafter.experiments import OpenAiChatExperiment

system_prompt = Prompt("You are a helpful assistant who responds to questions about the world")
hello_prompt = Prompt("Hello, what is the capital of France? Answer only with the city name.")
followup_prompt = Prompt("{city} sounds like a nice place to visit. What is the population of {city}?")
chain = Chain(
    system_prompt,
    (hello_prompt, "city"),
    (followup_prompt, "followup_response"),
)
experiment = OpenAiChatExperiment(
    chain,
    model_name=["gpt-4", "gpt-3.5-turbo"],
    temperature=[0.7, 1.5],
    presence_penalty=[0.1],
    frequency_penalty=[0.2],
)
experiment.run()
print(experiment.results)
```

### Output

```
Run 0 at 2023-08-04 09:02:51 with model parameters: {'model_name': 'gpt-4', 'temperature': 0.7, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: As of 2021, the estimated population of Paris is approximately 2.14 million people.

Run 0 at 2023-08-04 09:02:56 with model parameters: {'model_name': 'gpt-4', 'temperature': 1.5, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: As of 2021, the population of Paris is about 2.16 million people. However, please note that this data might vary slightly depending on the source.

Run 0 at 2023-08-04 09:02:58 with model parameters: {'model_name': 'gpt-3.5-turbo', 'temperature': 0.7, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: The population of Paris, as of 2020, is approximately 2.15 million people.

Run 0 at 2023-08-04 09:03:01 with model parameters: {'model_name': 'gpt-3.5-turbo', 'temperature': 1.5, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: As of 2021, the population of Paris is approximately 2.15 million.

[{'run_number': 0, 'timestamp': '2023-08-04 09:02:51', 'messages': [{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of 2021, the estimated population of Paris is approximately 2.14 million people.'}], 'model_name': 'gpt-4', 'temperature': 0.7, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}, {'run_number': 0, 'timestamp': '2023-08-04 09:02:56', 'messages': [{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of 2021, the population of Paris is about 2.16 million people. However, please note that this data might vary slightly depending on the source.'}], 'model_name': 'gpt-4', 'temperature': 1.5, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}, {'run_number': 0, 'timestamp': '2023-08-04 09:02:58', 'messages': [{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'The population of Paris, as of 2020, is approximately 2.15 million people.'}], 'model_name': 'gpt-3.5-turbo', 'temperature': 0.7, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}, {'run_number': 0, 'timestamp': '2023-08-04 09:03:01', 'messages': [{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of 2021, the population of Paris is approximately 2.15 million.'}], 'model_name': 'gpt-3.5-turbo', 'temperature': 1.5, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}]
```
