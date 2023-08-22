import asyncio
from collections import deque
import logging
from typing import TypedDict

from chaincrafter.loggers import DataLogger
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
        self._data_logger = None

    def set_data_logger(self, data_logger: DataLogger):
        self._data_logger = data_logger

    def run(self, chat_model: ChatModel, starting_input_vars: dict = {}) -> [Message]:
        """
        Runs the chain. The output of each prompt is passed to the next prompt as a starting input variable.

        Ensure that the keys of the starting input variables and the output are unique or they will be overwritten.

        :param chat_model: The LLM chat model to use.
        :param starting_input_vars: The starting input variables that are passed to the first prompt
            (not the system prompt)
        :return: The messages that were sent back and forth between the user and the system.
        """
        queue = deque(self._prompts_and_output_keys)

        input_vars = {key: value for key, value in starting_input_vars.items()}
        logging.debug(f"Starting input variables: {input_vars}")

        messages = [
            {"role": "system", "content": self._system_prompt.build(**input_vars)}
        ]
        while queue:
            human_prompt, output_key = queue.popleft()
            messages.append({"role": "user", "content": human_prompt.build(**input_vars)})
            content, response = chat_model.complete(messages)

            if output_key in input_vars:
                logging.warning(f"Overwriting input variable {output_key}")

            input_vars.update({output_key: content})
            messages.append({"role": "assistant", "content": content})

            self._log_data(chat_model, messages, response)
        return messages

    async def async_run(self, chat_model: ChatModel, starting_input_vars: dict = {}) -> [Message]:
        return await asyncio.to_thread(self.run, chat_model, starting_input_vars)

    def _log_data(self, chat_model: ChatModel, messages: [Message], response: dict):
        if self._data_logger is None:
            return
        print(response)
        self._data_logger.log(
            system_prompt=self._system_prompt._fmt_str,
            prompts=[prompt_output_key[0]._fmt_str for prompt_output_key in self._prompts_and_output_keys],
            messages=messages,
            model_name=chat_model._model_name,
            temperature=chat_model._temperature,
            top_p=chat_model._top_p,
            n=chat_model._n,
            stream=chat_model._stream,
            presence_penalty=chat_model._presence_penalty,
            frequency_penalty=chat_model._frequency_penalty,
            max_tokens=chat_model._max_tokens,
            stop_sequences=chat_model._stop,
            logit_bias=chat_model._logit_bias,
            response_id=response["id"],
            response_created_at=response["created"],
            response_model=response["model"],
            response_choices=response["choices"],
            usage_prompt_tokens=response["usage"]["prompt_tokens"],
            usage_completion_tokens=response["usage"]["completion_tokens"],
            usage_total_tokens=response["usage"]["total_tokens"],
        )
