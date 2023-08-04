# Based on the API from prompttools: https://prompttools.readthedocs.io/en/latest/experiment.html
from datetime import datetime
from itertools import product

import pandas as pd

from chaincrafter.chains import Chain
from chaincrafter.models import OpenAiChat


class Experiment:
    """
    An experiment that runs a chat model on a prompt. Generates all permutations of the variables provided.
    """

    model_class = None

    def __init__(self, messages: Chain, **model_params):
        self.messages = messages
        self.model_params = model_params
        self._model_params_product = None
        self._prepared = False
        self.results = []

    def _set_model_params(self, default_params: dict) -> None:
        """
        Sets default values for model parameters that are not specified in the experiment.
        :param default_params: A dict of default parameter values
        """
        for key, value in default_params.items():
            if key not in self.model_params:
                self.model_params[key] = value

    def prepare(self) -> None:
        """
        Prepares the experiment by generating all permutations of the model parameters.
        """
        self._model_params_product = product(*self.model_params.values())
        self._prepared = True

    def run(self, runs: int = 1) -> None:
        """
        Runs the experiment. Stores the results in self.results including the timestamp, run number, and messages and the model parameters.
        :param runs: The number of times to run the experiment
        """
        if not self._prepared:
            self.prepare()
        for run_number in range(runs):
            for model_params_values in self._model_params_product:
                model_params = dict(zip(self.model_params.keys(), model_params_values))
                model = self.model_class(**model_params)
                messages = self.messages.run(model)
                result = {
                    "run_number": run_number,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "messages": messages,
                }
                result.update(model_params)
                self.results.append(result)
                print(f"Run {run_number} at {result['timestamp']} with model parameters: {model_params}")
                for message in messages:
                    print(f"{message['role']}: {message['content']}")
                print()

    def to_csv(self):
        return pd.DataFrame(self.results).to_csv()

    def to_pandas_df(self):
        return pd.DataFrame(self.results)

    def to_json(self):
        return pd.DataFrame(self.results).to_json()

    def visualize(self):
        return pd.DataFrame(self.results)


class OpenAiChatExperiment(Experiment):
    model_class = OpenAiChat

    def __init__(self, messages, **model_params):
        super().__init__(messages, **model_params)
        self._set_model_params({
            "temperature": [1.0],
            "top_p": [1.0],
            "n": [1],
            "stream": [False],
            "stop": [None],
            "max_tokens": [None],
            "presence_penalty": [0.0],
            "frequency_penalty": [0.0],
            "logit_bias": [None],
        })
