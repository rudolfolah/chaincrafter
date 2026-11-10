import unittest

from chaincrafter import Prompt, extract_items_from_list


class TestPrompt(unittest.TestCase):
    def test_literal_prompt_preserves_braces_and_ignores_inputs(self):
        texts = [
            'function greet() { return {message: "hello"}; }',
            '{"name": "Ada", "options": {"enabled": true}}',
            "Hello {name}; keep {{braces}} and {0!r:>10}",
            "unfinished {",
            "unmatched }",
        ]
        for text in texts:
            with self.subTest(text=text):
                prompt = Prompt(text, format_template=False)
                self.assertEqual(prompt.build(), text)
                self.assertEqual(prompt.build(name="replacement"), text)

    def test_literal_prompt_skips_transformers_but_applies_modifiers_in_order(self):
        prompt = Prompt(
            "{name}",
            [str.upper, lambda text: text + " {suffix}"],
            format_template=False,
            name=int,
        )
        self.assertEqual(prompt.build(), "{NAME} {suffix}")
        self.assertEqual(prompt.build(name="not an integer"), "{NAME} {suffix}")

    def test_template_transforms_then_formats_then_modifies(self):
        prompt = Prompt(
            "{{result: {value:.2f}}}",
            [lambda text: text + " {literal}"],
            value=float,
        )
        self.assertEqual(prompt.build(value="3.5"), "{result: 3.50} {literal}")

    def test_template_errors_are_not_silently_treated_as_literal_text(self):
        for text, error in [("{missing}", KeyError), ("unfinished {", ValueError)]:
            with self.subTest(text=text):
                with self.assertRaises(error):
                    Prompt(text).build()


class TestListExtraction(unittest.TestCase):
    def test_preserves_colons_inside_items_and_skips_blank_lines(self):
        response = "\n1: Time: 12:30\n \n2: https://example.com:8080/path \n"
        self.assertEqual(
            extract_items_from_list(response),
            ["Time: 12:30", "https://example.com:8080/path"],
        )
