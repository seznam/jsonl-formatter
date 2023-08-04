import os
import unittest
from jsonl_formatter import load_and_deserialize, serialize, write, format
from collections import OrderedDict


class TestJSONLFormatter(unittest.TestCase):
    def setUp(self):
        self.jsonl_input_file = os.path.join(os.path.dirname(__file__), 'data.jsonl')
        self.jsonl_output_file = self.jsonl_input_file + '.tmp'
        self.expected_loaded_jsonl = [
            OrderedDict([("boolean", True), ("integer", 1), ("float", 1), ("string", "1"), ("object", OrderedDict([("b", "b1"), ("a", "a1"), ("c", "c1")])), ("array", [])]),
            OrderedDict([("boolean", False), ("integer", 11), ("float", 1.1), ("string", "11"), ("object", OrderedDict([("b", "b11"), ("a", "a11")])), ("optional", 11), ("array", [OrderedDict([("b", "b11.1"), ("a", "a11.1"), ("c", "c11.1")])])]),
            OrderedDict([("boolean", None), ("integer", 111), ("float", 1.11), ("string", "111"), ("object", OrderedDict([("b", "b111"), ("a", "a111")])), ("optional", 111), ("array", [OrderedDict([("b", "b111.1"), ("a", "a111.1")]), OrderedDict([("b", "b111.2"), ("a", "a111.2"), ("c", "c111.2")])])]),
        ]
        self.expected_serialized_jsonl = [
            '{"boolean": true,  "integer": 1,   "float": 1,    "string": "1",   "object": {"b": "b1",   "a": "a1",   "c": "c1"}, "array": []}',
            '{"boolean": false, "integer": 11,  "float": 1.1,  "string": "11",  "object": {"b": "b11",  "a": "a11"},             "array": [{"b": "b11.1",  "a": "a11.1",  "c": "c11.1"}],                                                "optional": 11}',
            '{"boolean": null,  "integer": 111, "float": 1.11, "string": "111", "object": {"b": "b111", "a": "a111"},            "array": [{"b": "b111.1", "a": "a111.1"},               {"b": "b111.2", "a": "a111.2", "c": "c111.2"}], "optional": 111}',
        ]

    def test_load_and_deserialize(self):
        self.assertEqual(
            load_and_deserialize(self.jsonl_input_file),
            self.expected_loaded_jsonl
        )

    def test_serialize(self):
        self.assertEqual(
            serialize(self.expected_loaded_jsonl),
            self.expected_serialized_jsonl
        )

    def test_write(self):
        write(self.jsonl_output_file, self.expected_serialized_jsonl)
        with open(self.jsonl_output_file, 'r') as file:
            self.assertEqual(file.read(), '\n'.join(self.expected_serialized_jsonl) + '\n')
