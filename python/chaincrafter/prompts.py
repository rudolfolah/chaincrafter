from typing import Callable


class Prompt:
    """
    A chat message prompt that is formatted with input variables and modified by prompt modifiers.
    """
    def __init__(self, fmt_str: str, prompt_modifiers: [Callable] = [], **input_vars_transformers: [dict[str, Callable]]):
        """
        A prompt is a string that is formatted with input variables and modified by prompt modifiers.

        :param fmt_str: The prompt string, with format variables in the form of {var_name}
        :param prompt_modifiers: Functions that modify the prompt string
        :param input_vars_transformers: The input variables and the functions that transform them
          such as `str` or `int` or `lambda x: x.lower()`.

        Usage:
        >>> prompt = Prompt("Add {a} and {b}", a=int, b=int)
        >>> prompt = Prompt(
        ...     fmt_str="Hello {name}!",
        ...     name=lambda x: x.capitalize(),
        ...     prompt_modifiers=[lambda x: x + " How are you?"],
        ... )
        """
        self._fmt_str = fmt_str
        self._prompt_modifiers = prompt_modifiers
        self._input_vars_transformers = input_vars_transformers

    def build(self, **input_vars):
        """
        Applies the input variable transformers to the input variables, then formats the prompt string.

        :param input_vars: key-value pairs of input variables
        :return: the formatted prompt string

        Usage:
        >>> prompt = Prompt(
        ...     fmt_str="Hello {name}!",
        ...     name=lambda x: x.capitalize(),
        ...     prompt_modifiers=[lambda x: x + " How are you?"],
        ... )
        >>> prompt.build(name="john")
        'Hello John! How are you?'
        """
        for input_var, transformer in self._input_vars_transformers.items():
            input_vars[input_var] = transformer(input_vars[input_var])
        formatted = self._fmt_str.format(**input_vars)
        for prompt_modifier in self._prompt_modifiers:
            formatted = prompt_modifier(formatted)
        return formatted


# Response Format Functions
def response_format_list(example_item_text: str) -> Callable[[str], str]:
    def formatter(formatted_message):
        items = '\n'.join([f"{i + 1}: {example_item_text} {i + 1}" for i in range(3)])
        return formatted_message + f"""
Format the answer in the following way:

{items}"""
    return formatter


def response_style(style_of: str) -> str:
    def formatter(formatted_message):
        return formatted_message + f"\nRespond in the style of {style_of}"
    return formatter


def response_length(short_or_long: str = "short", answer_or_paragraph: str = "sentence") -> str:
    def formatter(formatted_message):
        return formatted_message + f"\nRespond with a {short_or_long} {answer_or_paragraph}"
    return formatter


# Response Extraction Functions
def extract_items_from_list(response: str) -> [str]:
    return [item.split(":")[1].strip() for item in response.split("\n") if item.strip()]
