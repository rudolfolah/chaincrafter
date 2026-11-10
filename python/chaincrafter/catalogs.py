import logging
from typing import Callable, Dict

from chaincrafter.chains import Chain
from chaincrafter.prompts import Prompt
import yaml


class Catalog:
    """
    A catalog is a collection of chains and prompts stored in a YAML file.
    """
    def __init__(self):
        self.chains = {}
        self.prompts = {}
        self._prompt_fmt_strs = {}

    def load(self, path: str):
        """
        Loads a catalog from a YAML file.

        - Logs a warning if no chains are found.
        - Logs an error if a prompt is not found.
        :param path:
        :return:
        """
        with open(path, "r") as f:
            catalog = yaml.safe_load(f)
        self._load_prompts(catalog)
        self._load_chains(catalog)

    def _load_chains(self, catalog: dict):
        if "chains" not in catalog:
            logging.warning("No chains found in catalog.")
            return
        logging.info(f"Loading {len(catalog['chains'])} chains...")
        for name, chain in catalog["chains"].items():
            system_prompt_id, *prompts = chain
            system_prompt = self.prompts[system_prompt_id]
            prompts_and_output_keys = []
            for prompt in prompts:
                prompt_id = list(prompt.keys())[0]
                output_key = prompt[prompt_id]
                prompts_and_output_keys.append((self.prompts[prompt_id], output_key))
            self.chains[name] = Chain(
                system_prompt,
                *prompts_and_output_keys,
            )

    def _load_prompts(self, catalog: dict):
        if "prompts" not in catalog:
            logging.error("No prompts found in catalog.")
            return
        logging.info(f"Loading {len(catalog['prompts'])} prompts...")
        for name, fmt_str in catalog["prompts"].items():
            self.prompts[name] = Prompt(fmt_str)
            self._prompt_fmt_strs[name] = fmt_str

    def get_chain(self, chain_id: str) -> Chain:
        return self.chains[chain_id]

    def get_prompt(self, prompt_id: str, prompt_modifiers: [Callable] = [], **input_vars_transformers: [Dict[str, Callable]]) -> Prompt:
        """
        Gets a prompt from the catalog. If prompt_modifiers or input_vars_transformers are specified, a new prompt is
        created from the existing prompt format string.

        :param prompt_id:
        :param prompt_modifiers:
        :param input_vars_transformers:
        :return:
        """
        if len(prompt_modifiers) > 0 or len(input_vars_transformers) > 0:
            return Prompt(
                self._prompt_fmt_strs[prompt_id],
                prompt_modifiers,
                **input_vars_transformers
            )
        return self.prompts[prompt_id]

    # get prompt using [] syntax
    def __getitem__(self, prompt_id: str) -> Prompt:
        return self.get_prompt(prompt_id)
