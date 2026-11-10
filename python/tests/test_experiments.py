import io
import unittest
from contextlib import redirect_stdout

from chaincrafter.chains import Chain, Prompt
from chaincrafter.experiments import Experiment
from chaincrafter.models import ChatModel


class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.calls = []
        calls = self.calls

        class CountingChat(ChatModel):
            def __init__(self, temperature, model_name):
                self.temperature = temperature
                self.model_name = model_name

            def complete(self, messages):
                calls.append((self.model_name, self.temperature))
                return "{}:{}".format(self.model_name, self.temperature)

        self.model_class = CountingChat
        self.chain = Chain(Prompt("System"), (Prompt("Hello"), "answer"))
        self.combinations = [("first", 0.1), ("first", 0.9),
                             ("second", 0.1), ("second", 0.9)]

    def experiment(self, **params):
        experiment = Experiment(self.chain, **params)
        experiment.model_class = self.model_class
        return experiment

    def run_experiment(self, experiment, runs=1):
        with redirect_stdout(io.StringIO()):
            experiment.run(runs=runs)

    def assert_results(self, experiment, run_numbers):
        expected_combinations = self.combinations * (len(run_numbers) // 4)
        self.assertEqual(self.calls, expected_combinations)
        self.assertEqual(
            [(result["model_name"], result["temperature"]) for result in experiment.results],
            expected_combinations,
        )
        self.assertEqual([result["run_number"] for result in experiment.results], run_numbers)
        self.assertEqual(
            [result["messages"][-1] for result in experiment.results],
            [{"role": "assistant", "content": "{}:{}".format(name, temperature)}
             for name, temperature in expected_combinations],
        )

    def test_zero_runs_executes_no_combinations(self):
        experiment = self.experiment(model_name=["first", "second"], temperature=[0.1, 0.9])
        self.run_experiment(experiment, runs=0)
        self.assertEqual(self.calls, [])
        self.assertEqual(experiment.results, [])
        self.run_experiment(experiment)
        self.assert_results(experiment, [0] * 4)

    def test_each_repetition_executes_full_cartesian_product(self):
        experiment = self.experiment(model_name=["first", "second"], temperature=[0.1, 0.9])
        self.run_experiment(experiment, runs=3)
        self.assert_results(experiment, [0] * 4 + [1] * 4 + [2] * 4)

    def test_repeated_runs_reuse_generator_parameter_pools(self):
        experiment = self.experiment(
            model_name=(name for name in ["first", "second"]),
            temperature=(value for value in [0.1, 0.9]),
        )
        self.run_experiment(experiment, runs=2)
        self.run_experiment(experiment)
        self.assert_results(experiment, [0] * 4 + [1] * 4 + [0] * 4)

    def test_explicit_prepare_snapshots_sequence_parameters(self):
        names = ["first", "second"]
        temperatures = [0.1, 0.9]
        experiment = self.experiment(model_name=names, temperature=temperatures)
        experiment.prepare()
        names.append("third")
        temperatures.append(0.5)
        self.assertEqual(self.calls, [])
        self.run_experiment(experiment)
        self.run_experiment(experiment)
        self.assert_results(experiment, [0] * 8)
