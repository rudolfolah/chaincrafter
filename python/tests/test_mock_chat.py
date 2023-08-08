import unittest

from chaincrafter.chains import Chain, Prompt
from chaincrafter.models import MockChat


class TestMockChat(unittest.TestCase):
    def test_prompts(self):
        model = MockChat(0.9, 'mock')
        system_prompt = "Hello world!"
        expected = [
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': 'Hello?',
            },
            {
                'role': 'assistant',
                'content': 'Yes, hello'
            },
        ]
        model.mock_responses(["Yes, hello"])
        chain = Chain(Prompt(system_prompt), (Prompt("Hello?"), "output"))
        result = chain.run(model)
        self.assertListEqual(result, expected)
