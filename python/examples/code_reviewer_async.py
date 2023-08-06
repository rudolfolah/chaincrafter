import asyncio

from chaincrafter import Chain, Prompt
from chaincrafter.models import OpenAiChat

chat_model = OpenAiChat(
    temperature=0.7,
    model_name="gpt-4",
    presence_penalty=0.2,
    frequency_penalty=0.3,
    max_tokens=600,
)

review_prompts = [
    Prompt("I just put a lot of work into this code, can you please review it and offer suggestions for improvement? Do not write any code.\n```{diff}\n```", diff=str),
    Prompt("Thanks for the feedback! Can you think of anything else in the code that I will need to change to ensure it is ready for a production environment?"),
]
review_chain = Chain(
    Prompt("You are a helpful software engineer who is reviewing code and providing feedback. Your feedback is expected to be helpful and constructive, dripping with sarcasm."),
    (review_prompts[0], "feedback1"),
    (review_prompts[1], "feedback2"),
)

description_prompt = Prompt("Can you please describe the code changes at a high level, I want to use it for the pull request description.\n```{diff}\n```", diff=str)
description_chain = Chain(
    Prompt("You are a helpful software engineer who is reviewing code and helping me write a pull request description."),
    (description_prompt, "description"),
)


async def main():
    process = await asyncio.create_subprocess_shell(
        "git diff HEAD~2 HEAD~1", stdout=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    # convert bytes to string
    diff = stdout.decode().strip()
    starting_input_vars= {"diff": diff}
    results = await asyncio.gather(
        review_chain.async_run(chat_model, starting_input_vars),
        description_chain.async_run(chat_model, starting_input_vars),
    )
    for messages in results:
        for message in messages:
            if message['role'] != 'assistant':
                continue
            print(message['content'])
        print("\n\n")

asyncio.run(main())
