# Python

*[Code Reviewer Async](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/code_reviewer_async.py)*:
An example of using [the async API](./async.md) to run a chain of messages asynchronously. It uses a `git diff` as the material for a code review.
The results are a code review from a software engineer, a pull request description, and a description that could be used as a git commit message.

*[Comparing Code Models](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/comparing_code_models.py)*:
This example uses a prompt with the GPT-3.5 and GPT-4 models that will generate suggestions for code improvements and then apply the suggestions to the code.

*[Describe Topic Experiment](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/describe_topic_experiment.py)*:
Uses an [experiment](./experiments.md) to compare the responses from GPT-3.5 and GPT-4 for a chain of prompts that asks

*[Hello World](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/hello_world.py)*:
Chain of two prompts; the first asks for the capital of a country, the second asks for the city's population.

*[Hello World Async](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/hello_world_async.py)*:
Same as *Hello World*, however it uses [the async API](./async.md) to run two chains asynchronously. It asks for the capital cities of two countries and then asks for the population of each.

*[Hello World Experiment](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/hello_world_experiment.py)*:
Same as *Hello World*, however it uses an [experiment](./experiments.md) to run the chain with two different models and different model parameters. Also prints out the output in different formats (CSV, JSON, Pandas DataFrame).

*[Hello World Catalog](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/hello_world_catalog.py)*:
Same as *Hello World*, however it loads the prompts and chain from a catalog to run the chain.

*[Interesting Facts](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/interesting_facts.py)*:
Demonstrates using [methods to transform and modify prompts and to extract data from responses](./api.md). It will prompt for a list of facts about a topic, which are formatted in a particular way, and then it extracts the first fact and passes it along to the next prompt. The response styles are changed between the prompts, the response length is added to the prompt, and the list format to be used is also part of the prompt.

*[Interesting Facts Catalog](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/interesting_facts_catalog.py)*:
Same as *Interesting Facts*, loads the prompts from a catalog and adds a few prompt modifiers.

*[Math](https://github.com/rudolfolah/chaincrafter/blob/main/python/examples/math_example.py)*:
An example based on the math example from MiniChain. It uses few-shot training prompt to include math questions and the code that solves them. The prompt asks for the Python code to solve the given math problem and then runs the code to produce the answer.

# JavaScript/TypeScript

*work in progress*