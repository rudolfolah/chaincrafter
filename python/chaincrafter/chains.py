import asyncio
from collections import deque
from typing import TypedDict

from chaincrafter.models import ChatModel
from chaincrafter.prompts import Prompt


Message = TypedDict('Message', {'role': str, 'content': str})


class Chain:
    def __init__(self, system_prompt: Prompt, *prompts_and_output_keys: [Prompt, str]):
        """
        Sets up the system prompt and a chain of prompts and output keys.
        :param system_prompt: The prompt that sets up the system and it gives it some starting information.
        :param prompts_and_output_keys: A list of tuples of prompts and output keys. The prompts are prompts for the
            user, they specify their own input keys. The output keys are the keys that the user's input will be stored
            in.
        """
        self._system_prompt = system_prompt
        self._prompts_and_output_keys = prompts_and_output_keys

    def run(self, chat_model: ChatModel, starting_input_vars: dict = {}) -> [Message]:
        """
        Runs the chain.
        :param chat_model: The LLM chat model to use.
        :param starting_input_vars: The starting input variables that are passed to the first prompt
            (not the system prompt)
        :return: The messages that were sent back and forth between the user and the system.
        """
        queue = deque(self._prompts_and_output_keys)
        input_vars = {key: value for key, value in starting_input_vars.items()}
        messages = [
            {"role": "system", "content": self._system_prompt.build(**input_vars)}
        ]
        while queue:
            human_prompt, output_key = queue.popleft()
            messages.append({"role": "user", "content": human_prompt.build(**input_vars)})
            response = chat_model.complete(messages)
            input_vars = {output_key: response}
            messages.append({"role": "assistant", "content": response})
        return messages

    async def async_run(self, chat_model: ChatModel, starting_input_vars: dict = {}) -> [Message]:
        return await asyncio.to_thread(self.run, chat_model, starting_input_vars)
