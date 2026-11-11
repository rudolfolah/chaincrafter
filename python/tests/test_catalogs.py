import os
import tempfile
import unittest
from types import SimpleNamespace

import yaml

from chaincrafter.catalogs import Catalog
from chaincrafter.prompts import Prompt


class TestCatalog(unittest.TestCase):
    def load_catalog(self, contents):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "catalog.yaml")
            with open(path, "w", encoding="utf-8") as stream:
                yaml.safe_dump(contents, stream)
            catalog = Catalog()
            catalog.load(path)
        return catalog

    def test_prompt_only_catalog_loads_usable_prompts(self):
        catalog = self.load_catalog({"prompts": {"greeting": "Hello {name}!"}})
        self.assertEqual(catalog.get_prompt("greeting").build(name="Ada"), "Hello Ada!")
        self.assertEqual(catalog["greeting"].build(name="Grace"), "Hello Grace!")

    def test_default_formatting_matches_direct_prompt(self):
        cases = [
            ("{value:.2f}", {"value": 3.125}),
            ("{value:04d}", {"value": 7}),
            ("{items[0]} / {record[name]}", {"items": ["first"], "record": {"name": "Ada"}}),
            ("{person.name}", {"person": SimpleNamespace(name="Ada")}),
            ("{value:{width}.{precision}f}", {"value": 3.125, "width": 8, "precision": 2}),
            ("{{literal}} {value!r}", {"value": "Ada"}),
            ("plain text", {}),
        ]
        for fmt_str, inputs in cases:
            with self.subTest(fmt_str=fmt_str):
                catalog = self.load_catalog({"prompts": {"example": fmt_str}})
                self.assertEqual(catalog["example"].build(**inputs), Prompt(fmt_str).build(**inputs))

    def test_explicit_transformers_and_modifiers_preserve_other_input_types(self):
        fmt_str = "{value:.1f} {count:03d} {items[0]}"
        catalog = self.load_catalog({"prompts": {"example": fmt_str}})
        inputs = {"value": "2.5", "count": 7, "items": ["ready"]}
        modifiers = [str.upper, lambda text: "[" + text + "]"]
        overridden = catalog.get_prompt("example", modifiers, value=float)
        self.assertEqual(overridden.build(**inputs), "[2.5 007 READY]")
        self.assertEqual(
            catalog.get_prompt("example", value=float).build(**inputs),
            "2.5 007 ready",
        )
        self.assertEqual(
            catalog.get_prompt("example", modifiers).build(value=2.5, count=7, items=["ready"]),
            "[2.5 007 READY]",
        )
        self.assertEqual(catalog["example"].build(value=3.5, count=8, items=["original"]), "3.5 008 original")

    def test_missing_prompts_with_empty_chains_is_accepted(self):
        with self.assertLogs(level="ERROR"):
            catalog = self.load_catalog({"chains": {}})
        with self.assertRaises(KeyError):
            catalog.get_prompt("missing")

    def test_yaml_chain_formats_prompts_and_passes_outputs(self):
        catalog = self.load_catalog({
            "prompts": {
                "system": "Use {precision:d} decimals",
                "first": "Value {value:.2f}",
                "second": "Previous {answer}; {items[0]}",
            },
            "chains": {"example": ["system", {"first": "answer"}, {"second": "final"}]},
        })

        class RecordingModel:
            def __init__(self):
                self.requests = []

            def complete(self, messages):
                self.requests.append([dict(message) for message in messages])
                return "response {}".format(len(self.requests))

        model = RecordingModel()
        messages = catalog.get_chain("example").run(
            model, {"precision": 2, "value": 3.125, "items": ["done"]}
        )
        self.assertEqual(messages, [
            {"role": "system", "content": "Use 2 decimals"},
            {"role": "user", "content": "Value 3.12"},
            {"role": "assistant", "content": "response 1"},
            {"role": "user", "content": "Previous response 1; done"},
            {"role": "assistant", "content": "response 2"},
        ])
        self.assertEqual(model.requests[0], messages[:2])
        self.assertEqual(model.requests[1], messages[:4])
