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

    def mock_responses(self, messages: [dict]):
        self._mock_responses = messages

    def complete(self, messages):
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
    def __init__(self, temperature, model_name):
        super().__init__(temperature, model_name)
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key is None:
            logging.error("OPENAI_API_KEY environment variable is not set")
            sys.exit(1)
        self._temperature = temperature
        self._model_name = model_name
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
        completion = openai.ChatCompletion.create(
            model=self._model_name,
            temperature=self._temperature,
            messages=messages,
        )
        logging.debug("OpenAI API call complete")
        self.usage["prompt_tokens"] += completion.usage["prompt_tokens"]
        self.usage["completion_tokens"] += completion.usage["completion_tokens"]
        self.usage["total_tokens"] += completion.usage["total_tokens"]
        return completion.choices[0].message["content"]

    def show_usage(self):
        print(f"Prompt tokens: {self.usage['prompt_tokens']}")
        print(f"Completion tokens: {self.usage['completion_tokens']}")
        print(f"Total tokens: {self.usage['total_tokens']}")
