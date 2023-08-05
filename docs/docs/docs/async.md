Chains can be run async by using `async_run` instead of `run`. This uses the asyncio library to run the chain in parallel.

* be aware of rate limits with OpenAI and other APIs
* for local models, be aware of CPU and memory usage

# Running chains async with `asyncio`

Use `asyncio.gather` to run multiple chains concurrently with the `async_run` method. The way this works is that it uses threads to wrap the blocking I/O calls that are made to the models.

```python
import asyncio

async def concurrent_runs():
    chat_model = OpenAiChat(temperature=0.65, model_name="gpt-3.5-turbo")
    system_prompt = Prompt("You are a helpful assistant who responds to questions about the world")
    chain_a = Chain(system_prompt, Prompt("What goes with French fries?"))
    chain_b = Chain(system_prompt, Prompt("Is poutine a Canadian dish?"))

    results = await asyncio.gather(
        chain_a.async_run(chat_model),
        chain_b.async_run(chat_model),
        # ... more chains
    )

    for messages in results:
        for message in messages:
            print(f"{message['role']}: {message['content']}")

asyncio.run(concurrent_runs())
```

# Example

## Code

```python
import asyncio

from chaincrafter import Chain, Prompt
from chaincrafter.models import OpenAiChat

chat_model = OpenAiChat(
    temperature=0.9,
    model_name="gpt-3.5-turbo",
    presence_penalty=0.1,
    frequency_penalty=0.2,
)


def make_chain(country):
    system_prompt = Prompt("You are a helpful assistant who responds to questions about the world")
    followup_prompt = Prompt("{city} sounds like a nice place to visit. What is the population of {city}?")
    hello_prompt = Prompt(f"Hello, what is the capital of {country}? Answer only with the city name.")
    return Chain(
        system_prompt,
        (hello_prompt, "city"),
        (followup_prompt, "followup_response"),
    )


async def main():
    chain_france = make_chain("France")
    chain_china = make_chain("China")
    results = await asyncio.gather(
        chain_france.async_run(chat_model),
        chain_china.async_run(chat_model),
    )
    for messages in results:
        for message in messages:
            print(f"{message['role']}: {message['content']}")

asyncio.run(main())
```

## Output

```
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of France? Answer only with the city name.
assistant: Paris
user: Paris sounds like a nice place to visit. What is the population of Paris?
assistant: As of 2021, the population of Paris is approximately 2.2 million people.
system: You are a helpful assistant who responds to questions about the world
user: Hello, what is the capital of China? Answer only with the city name.
assistant: Beijing.
user: Beijing. sounds like a nice place to visit. What is the population of Beijing.?
assistant: The population of Beijing is over 21 million people.
```
