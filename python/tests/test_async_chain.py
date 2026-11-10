import asyncio
from contextvars import ContextVar
import unittest

from chaincrafter import Chain, Prompt
from chaincrafter.models import MockChat


class TestAsyncChain(unittest.TestCase):
    def test_async_chain_preserves_context_and_input_variables(self):
        city = ContextVar("city")

        class ContextChat(MockChat):
            def complete(self, messages):
                return city.get()

        async def run():
            city.set("Paris")
            chain = Chain(Prompt("Answer briefly"), (Prompt("Capital of {country}?"), "city"))
            return await chain.async_run(ContextChat(0.7, "mock"), {"country": "France"})

        self.assertEqual(asyncio.run(run()), [
            {"role": "system", "content": "Answer briefly"},
            {"role": "user", "content": "Capital of France?"},
            {"role": "assistant", "content": "Paris"},
        ])
