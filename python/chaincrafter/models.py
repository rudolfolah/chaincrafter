import logging
import os
import subprocess
import sys


# Base Model
class ChatModel:
    """
    A base class for chat models.
    """
    def __init__(self, temperature: float, model_name: str):
        pass

    def complete(self, messages: [dict]) -> str:
        pass

    def show_usage(self):
        pass


# Mock Models
class MockChat(ChatModel):
    def __init__(self, temperature, model_name):
        self._temperature = temperature
        self._model_name = model_name
        self._mock_responses = []

    def mock_responses(self, messages: [str]):
        self._mock_responses = messages

    def complete(self, messages: [dict]) -> str:
        return self._mock_responses.pop(0)


# Integration Models
class LlamaCppChat(ChatModel):
    """
    A chat model that uses the llama.cpp library.

    Requires that the LLAMA_CPP_PATH environment variable is set.

    Example usage:
    >>> model = LlamaCppChat(0.9, '/path/to/model.bin')
    >>> model.complete([{ 'role': 'system', 'content': 'Hello world!' }])
    >>> model = LlamaCppChat(0.9, '/Users/rudolfo/Library/Application Support/nomic.ai/GPT4All/nous-hermes-13b.ggmlv3.q4_0.bin')
    >>> model.complete([{ 'role': 'system', 'content': 'Hello world!' }, { 'role': 'user', 'content': 'What are five different trees in North America?' }])
    """

    def __init__(self, temperature, model_name):
        """

        :param temperature:
        :param model_name: The path to the model to load
        """
        self._bin_path = os.getenv("LLAMA_CPP_PATH")
        self._temperature = temperature
        self._model_name = model_name

        # for testing
        self._bin_path = '/Users/rudolfo/Workspace/llama.cpp/main'
        self._model_name = '/Users/rudolfo/Library/Application Support/nomic.ai/GPT4All/nous-hermes-13b.ggmlv3.q4_0.bin'

    def complete(self, messages):
        _process: subprocess.Popen = subprocess.Popen(
            [self._bin_path, '--model', self._model_name, '--interactive-first', '--temp', str(self._temperature), '-ngl', '1'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        starting_prompt = rf"""Transcript of a dialog between a user and an assistant named System. System is a person who is helpful, kind, honest and provides immediate and precise answers without having to do any additional research. {messages[0]['content']}\
User: Hello, System.\
System: Hello! How can I assist you today?\
User: {messages[1]['content']}\
System: /"""
        _process.communicate(input=(starting_prompt).encode())
        print(_process.communicate())


class OpenAiChat(ChatModel):
    """
    A chat model that uses OpenAI's API.

    Requires that the OPENAI_API_KEY environment variable is set.
    """
    def __init__(
            self,
            temperature: float,
            model_name: str,
            top_p: float = 1.0,
            n: int = 1,
            stream: bool = False,
            stop: [str] = None,
            max_tokens: int = None,
            presence_penalty: float = 0.0,
            frequency_penalty: float = 0.0,
            logit_bias: dict = None,
    ):
        super().__init__(temperature, model_name)
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key is None:
            logging.error("OPENAI_API_KEY environment variable is not set")
            sys.exit(1)
        self._temperature = temperature
        self._model_name = model_name
        self._top_p = top_p
        self._n = n
        self._stream = stream
        self._stop = stop
        self._max_tokens = max_tokens
        self._presence_penalty = presence_penalty
        self._frequency_penalty = frequency_penalty
        self._logit_bias = logit_bias
        logging.info(f"Using OpenAI model {self._model_name}, temperature {self._temperature}")
        self.usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def complete(self, messages: [dict]):
        """
        Completes a chat using OpenAI's API.

        :param messages: A list of messages to send to the chat model
        :return:
        """
        import openai
        logging.debug("Calling OpenAI API")
        kwargs = {
            "model": self._model_name,
            "temperature": self._temperature,
            "messages": messages,
            "top_p": self._top_p,
            "n": self._n,
            "stream": self._stream,
            "presence_penalty": self._presence_penalty,
            "frequency_penalty": self._frequency_penalty,
        }
        if self._stop:
            kwargs["stop"] = self._stop
        if self._max_tokens:
            kwargs["max_tokens"] = self._max_tokens
        if self._logit_bias:
            kwargs["logit_bias"] = self._logit_bias
        completion = openai.ChatCompletion.create(**kwargs)
        logging.debug("OpenAI API call complete")
        self.usage["prompt_tokens"] += completion.usage["prompt_tokens"]
        self.usage["completion_tokens"] += completion.usage["completion_tokens"]
        self.usage["total_tokens"] += completion.usage["total_tokens"]
        return completion.choices[0].message["content"]

    def show_usage(self):
        print(f"Prompt tokens: {self.usage['prompt_tokens']}")
        print(f"Completion tokens: {self.usage['completion_tokens']}")
        print(f"Total tokens: {self.usage['total_tokens']}")
