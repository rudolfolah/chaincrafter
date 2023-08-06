Experiments are a way to run a set of prompt chains with a variety of model parameters and compare the results. This is useful for finding the best model parameters for a given prompt chain. It is also useful to store and compare the results at later points in time.

# Experiment

An experiment that runs a chat model on a prompt. Generates all permutations of the variables provided.

* `Experiment(chain, **model_params)`: Create an experiment with the given prompts `Chain` and the model parameters
* `Experiment.run(runs=1)`: Run the experiment
* `Experiment.model_class`: The `ChatModel` subclass used in the experiment
* `Experiment.results`: The results of the experiment
* `Experiment.prepare()`: Prepare the experiment by generating the Cartesian product of the model parameters
* `Experiment.to_csv()`: Returns the results as a CSV string
* `Experiment.to_json()`: Returns the results as a JSON string
* `Experiment.to_pandas_df()`: Returns the results as a Pandas DataFrame
* `Experiment.visualize()`: Returns the results as a Pandas DataFrame

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
# CSV Output
print(experiment.to_csv())
# JSON Output
print(experiment.to_json())
# Pandas DataFrame Output
print(experiment.to_pandas_df())
# Pandas DataFrame Visualize
print(experiment.visualize())
```

### Output

```
Run 0 at 2023-08-04 09:42:17 with model parameters: {'model_name': 'gpt-4', 'temperature': 0.7, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: As of 2021, the population of Paris is approximately 2.16 million people.

Run 0 at 2023-08-04 09:42:24 with model parameters: {'model_name': 'gpt-4', 'temperature': 1.5, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: As of the latest data from 2021, the population of Paris is approximately 2.14 million people in the city proper. Note that the population of the larger Paris Metropolitan area is considerably higher.

Run 0 at 2023-08-04 09:42:25 with model parameters: {'model_name': 'gpt-3.5-turbo', 'temperature': 0.7, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: The population of Paris is approximately 2.2 million people.

Run 0 at 2023-08-04 09:42:27 with model parameters: {'model_name': 'gpt-3.5-turbo', 'temperature': 1.5, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: As of 2021, the estimated population of Paris is over 2.1 million residents in the city proper area.

[{'run_number': 0, 'timestamp': '2023-08-04 09:42:17', 'messages': [{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of 2021, the population of Paris is approximately 2.16 million people.'}], 'model_name': 'gpt-4', 'temperature': 0.7, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}, {'run_number': 0, 'timestamp': '2023-08-04 09:42:24', 'messages': [{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of the latest data from 2021, the population of Paris is approximately 2.14 million people in the city proper. Note that the population of the larger Paris Metropolitan area is considerably higher.'}], 'model_name': 'gpt-4', 'temperature': 1.5, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}, {'run_number': 0, 'timestamp': '2023-08-04 09:42:25', 'messages': [{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'The population of Paris is approximately 2.2 million people.'}], 'model_name': 'gpt-3.5-turbo', 'temperature': 0.7, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}, {'run_number': 0, 'timestamp': '2023-08-04 09:42:27', 'messages': [{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of 2021, the estimated population of Paris is over 2.1 million residents in the city proper area.'}], 'model_name': 'gpt-3.5-turbo', 'temperature': 1.5, 'presence_penalty': 0.1, 'frequency_penalty': 0.2, 'top_p': 1.0, 'n': 1, 'stream': False, 'stop': None, 'max_tokens': None, 'logit_bias': None}]
,run_number,timestamp,messages,model_name,temperature,presence_penalty,frequency_penalty,top_p,n,stream,stop,max_tokens,logit_bias
0,0,2023-08-04 09:42:17,"[{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of 2021, the population of Paris is approximately 2.16 million people.'}]",gpt-4,0.7,0.1,0.2,1.0,1,False,,,
1,0,2023-08-04 09:42:24,"[{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of the latest data from 2021, the population of Paris is approximately 2.14 million people in the city proper. Note that the population of the larger Paris Metropolitan area is considerably higher.'}]",gpt-4,1.5,0.1,0.2,1.0,1,False,,,
2,0,2023-08-04 09:42:25,"[{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'The population of Paris is approximately 2.2 million people.'}]",gpt-3.5-turbo,0.7,0.1,0.2,1.0,1,False,,,
3,0,2023-08-04 09:42:27,"[{'role': 'system', 'content': 'You are a helpful assistant who responds to questions about the world'}, {'role': 'user', 'content': 'Hello, what is the capital of France? Answer only with the city name.'}, {'role': 'assistant', 'content': 'Paris'}, {'role': 'user', 'content': 'Paris sounds like a nice place to visit. What is the population of Paris?'}, {'role': 'assistant', 'content': 'As of 2021, the estimated population of Paris is over 2.1 million residents in the city proper area.'}]",gpt-3.5-turbo,1.5,0.1,0.2,1.0,1,False,,,

{"run_number":{"0":0,"1":0,"2":0,"3":0},"timestamp":{"0":"2023-08-04 09:42:17","1":"2023-08-04 09:42:24","2":"2023-08-04 09:42:25","3":"2023-08-04 09:42:27"},"messages":{"0":[{"role":"system","content":"You are a helpful assistant who responds to questions about the world"},{"role":"user","content":"Hello, what is the capital of France? Answer only with the city name."},{"role":"assistant","content":"Paris"},{"role":"user","content":"Paris sounds like a nice place to visit. What is the population of Paris?"},{"role":"assistant","content":"As of 2021, the population of Paris is approximately 2.16 million people."}],"1":[{"role":"system","content":"You are a helpful assistant who responds to questions about the world"},{"role":"user","content":"Hello, what is the capital of France? Answer only with the city name."},{"role":"assistant","content":"Paris"},{"role":"user","content":"Paris sounds like a nice place to visit. What is the population of Paris?"},{"role":"assistant","content":"As of the latest data from 2021, the population of Paris is approximately 2.14 million people in the city proper. Note that the population of the larger Paris Metropolitan area is considerably higher."}],"2":[{"role":"system","content":"You are a helpful assistant who responds to questions about the world"},{"role":"user","content":"Hello, what is the capital of France? Answer only with the city name."},{"role":"assistant","content":"Paris"},{"role":"user","content":"Paris sounds like a nice place to visit. What is the population of Paris?"},{"role":"assistant","content":"The population of Paris is approximately 2.2 million people."}],"3":[{"role":"system","content":"You are a helpful assistant who responds to questions about the world"},{"role":"user","content":"Hello, what is the capital of France? Answer only with the city name."},{"role":"assistant","content":"Paris"},{"role":"user","content":"Paris sounds like a nice place to visit. What is the population of Paris?"},{"role":"assistant","content":"As of 2021, the estimated population of Paris is over 2.1 million residents in the city proper area."}]},"model_name":{"0":"gpt-4","1":"gpt-4","2":"gpt-3.5-turbo","3":"gpt-3.5-turbo"},"temperature":{"0":0.7,"1":1.5,"2":0.7,"3":1.5},"presence_penalty":{"0":0.1,"1":0.1,"2":0.1,"3":0.1},"frequency_penalty":{"0":0.2,"1":0.2,"2":0.2,"3":0.2},"top_p":{"0":1.0,"1":1.0,"2":1.0,"3":1.0},"n":{"0":1,"1":1,"2":1,"3":1},"stream":{"0":false,"1":false,"2":false,"3":false},"stop":{"0":null,"1":null,"2":null,"3":null},"max_tokens":{"0":null,"1":null,"2":null,"3":null},"logit_bias":{"0":null,"1":null,"2":null,"3":null}}
   run_number            timestamp                                           messages     model_name  temperature  presence_penalty  frequency_penalty  top_p  n  stream  stop max_tokens logit_bias
0           0  2023-08-04 09:42:17  [{'role': 'system', 'content': 'You are a help...          gpt-4          0.7               0.1                0.2    1.0  1   False  None       None       None
1           0  2023-08-04 09:42:24  [{'role': 'system', 'content': 'You are a help...          gpt-4          1.5               0.1                0.2    1.0  1   False  None       None       None
2           0  2023-08-04 09:42:25  [{'role': 'system', 'content': 'You are a help...  gpt-3.5-turbo          0.7               0.1                0.2    1.0  1   False  None       None       None
3           0  2023-08-04 09:42:27  [{'role': 'system', 'content': 'You are a help...  gpt-3.5-turbo          1.5               0.1                0.2    1.0  1   False  None       None       None
   run_number            timestamp                                           messages     model_name  temperature  presence_penalty  frequency_penalty  top_p  n  stream  stop max_tokens logit_bias
0           0  2023-08-04 09:42:17  [{'role': 'system', 'content': 'You are a help...          gpt-4          0.7               0.1                0.2    1.0  1   False  None       None       None
1           0  2023-08-04 09:42:24  [{'role': 'system', 'content': 'You are a help...          gpt-4          1.5               0.1                0.2    1.0  1   False  None       None       None
2           0  2023-08-04 09:42:25  [{'role': 'system', 'content': 'You are a help...  gpt-3.5-turbo          0.7               0.1                0.2    1.0  1   False  None       None       None
3           0  2023-08-04 09:42:27  [{'role': 'system', 'content': 'You are a help...  gpt-3.5-turbo          1.5               0.1                0.2    1.0  1   False  None       None       None
```
