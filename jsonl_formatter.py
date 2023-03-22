#!/usr/bin/env python3
import argparse
import logging
import os
from collections import OrderedDict
import json
import sys


class JSONLFormatter:
    def __init__(self):
        self.json_serialize = json.dumps
        self.json_deserialize = lambda json_line: json.loads(json_line, object_pairs_hook=OrderedDict)
        self.key_not_found = KeyError()

    def format(self, path: str) -> None:
        try:
            deserialized = self._load_and_deserialize(path)
            logging.debug('File `%s` has been loaded and deserialized', path)
        except IOError as load_error:
            raise Exception(f'Failed to load file `{path}`\n\t{load_error}')
        except Exception as deserialize_exception:
            raise Exception(f'Failed to deserialize file `{path}`\n\t{deserialize_exception}')
        serialized = self._serialize(deserialized)
        logging.debug('Deserialized file `%s` has been serialized', path)
        try:
            self._write(path, serialized)
            logging.debug('Serialized file `%s` has been written', path)
        except IOError as write_error:
            raise Exception(f'Failed to write file `{path}`\n\t{write_error}')

    def _load_and_deserialize(self, path: str) -> list:
        with open(path, 'r') as jsonl_file:
            return [self.json_deserialize(json_line) for json_line in jsonl_file.readlines()]

    @staticmethod
    def _write(path: str, serialized: list) -> None:
        with open(path, 'w') as jsonl_file:
            jsonl_file.write('\n'.join(serialized) + ('\n' if serialized else ''))

    def _serialize(self, data_objects: list, **kwargs) -> list:
        if not data_objects:
            return []
        keys = kwargs.get('keys', None)
        is_array = kwargs.get('is_array', None)
        if keys is None:
            keys = self._get_keys(data_objects)
        if is_array is None:
            is_array = isinstance(data_objects[0], list)
        serialized = self._open_lines(data_objects, is_array)
        for key in keys:
            serialized = self._serialize_key(serialized, data_objects, key, is_array)
        return self._close_lines(serialized, is_array)

    @staticmethod
    def _open_lines(data_objects: list, is_array: bool) -> list:
        return ['[' if is_array else '{' for _ in data_objects]

    def _serialize_key(self, lines: list, data_objects: list, key: str, is_array: bool) -> list:
        values = [self._get_value(data_object, key) for data_object in data_objects]
        serialized = []
        max_length = 0
        cache = []
        for index, value in enumerate(values):
            if value is self.key_not_found:
                key_value = ''
            else:
                if isinstance(value, OrderedDict) or isinstance(value, list):
                    key_value = self._serialize_key_object(key, value, values, index, is_array, cache)
                else:
                    key_value = self._serialize_key_value(key, value, is_array)
                key_value += ', '
            max_length = max(max_length, len(key_value))
            serialized.append(key_value)
        return [
            lines[index] + key_value + ''.rjust(max_length - len(key_value), ' ')
            for index, key_value in enumerate(serialized)
        ]

    def _serialize_key_object(self, key: str, data_object, data_objects: list, index: int, is_array: bool, cache: list) -> str:
        if not cache:
            cache.extend(self._serialize(
                data_objects,
                keys=self._get_keys(data_objects),
                is_array=isinstance(data_object, list),
            ))
        serialized = cache[index]
        if is_array:
            return serialized
        else:
            return self.json_serialize({key: '?'})[1:-1].replace('"?"', serialized)

    def _serialize_key_value(self, key: str, value, is_array: bool) -> str:
        if is_array:
            return self.json_serialize(value)
        else:
            return self.json_serialize({key: value})[1:-1]

    @staticmethod
    def _close_lines(lines: list, is_array: bool) -> list:
        return [line.rstrip(' ').rstrip(',') + (']' if is_array else '}') for line in lines]

    @staticmethod
    def _get_keys(data_objects: list) -> list:
        keys = []
        for data_object in data_objects:
            data_object_keys = []
            if isinstance(data_object, list):
                data_object_keys = range(len(data_object))
            elif hasattr(data_object, 'keys'):
                data_object_keys = data_object.keys()
            # keep order of keys
            for key in data_object_keys:
                if key not in keys:
                    keys.append(key)
        return keys

    def _get_value(self, data_object, key: str):
        try:
            return data_object[key]
        except (KeyError, IndexError, TypeError, AttributeError):
            return self.key_not_found


def format_jsonl_files(jsonl_files: list) -> None:
    is_ok = True
    jsonl_formatter = JSONLFormatter()
    for jsonl_file in jsonl_files:
        try:
            jsonl_formatter.format(jsonl_file)
            logging.info('File `%s` has been formatted', jsonl_file)
        except Exception as exception:
            is_ok = False
            logging.error('%s', exception)
    if not jsonl_files:
        logging.warning('No files to format')
        sys.exit(os.EX_NOINPUT)
    elif is_ok:
        logging.info('All files have been formatted')
        sys.exit(os.EX_OK)
    else:
        logging.info('Some files could not be formatted')
        sys.exit(os.EX_IOERR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog='For more information visit https://github.com/seznam/jsonl-formatter')
    parser.add_argument('jsonl_files', metavar='jsonl_file', type=str, nargs='+', help='JSON Lines files')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Make it more talkative')
    args = parser.parse_args()

    logging.basicConfig(
        level=(logging.WARNING if args.verbose == 0 else logging.INFO if args.verbose == 1 else logging.DEBUG),
        format="%(message)s"
    )

    format_jsonl_files(args.jsonl_files)
