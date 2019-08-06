import json
import yaml
import os.path
from gendiff.formatters import string, plain, m_json
from gendiff.constants import *


JSON_FORMAT = '.json'
YAML_FORMAT = '.yml'

FORMAT_STRING, FORMAT_PLAIN, FORMAT_JSON = ('string', 'plain', 'json')

BUILDERS_FORMATS = {
    FORMAT_STRING: string,
    FORMAT_PLAIN: plain,
    FORMAT_JSON: m_json
}


def switch_case(case, dict):
    return dict.get(case, f'No case {case} in dictionary')


def get_file(file_format, file_content):
    if file_format == JSON_FORMAT:
        with open(file_content, "r") as src_file:
            file = json.load(src_file)
    if file_format == YAML_FORMAT:
        with open(file_content, "r") as src_file:
            file = yaml.load(src_file, yaml.Loader)
    return file


def get_error_message(file_name=None, file_format=None):
    return (
        f'The format of {file_name} "{file_format}" '
        'is not supported by this program. '
        'Try to compare "json" or "yml" formats.'
    )


def get_diff(first_file, second_file, format):
    format = FORMAT_STRING if format is None else format
    first_file_format = os.path.splitext(first_file)[-1]
    second_file_format = os.path.splitext(second_file)[-1]
    if (first_file_format != '.json' and first_file_format != '.yml'):
        message = get_error_message(
            first_file,
            first_file_format
        )
        return print(message)
    if (second_file_format != '.json' and second_file_format != '.yml'):
        message = get_error_message(
            second_file,
            second_file_format
        )
        return print(message)
    file1 = get_file(first_file_format, first_file)
    file2 = get_file(second_file_format, second_file)
    ast = build_ast(file1, file2)
    result = build_representation(format, ast)
    return result


def build_representation(format, ast):
    builder = BUILDERS_FORMATS[format]
    return builder.build_representation(ast)


def build_nested(node):
    nested_ast = {}
    for k in node:
        value = build_nested(node[k]) if isinstance(node[k], dict) else node[k]
        nested_ast[k] = {
            'type': UNCHANGED,
            'value': value
        }
    return nested_ast


def build_ast(file1, file2, path=''):
    ast = {}
    if not file1 and not file2:
        print('No data to compare, the files are empty')
        return
    for k in file1:
        if k in file2:
            if isinstance(file1[k], dict) and isinstance(file2[k], dict):
                ast[k] = {
                    'type': UNCHANGED,
                    'children': build_ast(file1[k], file2[k], f'{path}{k}.')
                }
                continue
            if file1[k] == file2[k]:
                ast[k] = {
                    'type': UNCHANGED,
                    'value': file1[k]
                }
                continue
            if file1[k] != file2[k]:
                ast[k] = {
                    'type': CHANGED,
                    'path': f'{path}{k}',
                    'old_value': file1[k],
                    'new_value': file2[k]
                }
                continue
        if isinstance(file1[k], dict):
            ast[k] = {
                'type': REMOVED,
                'path': f'{path}{k}',
                'children': build_nested(file1[k])
            }
            continue
        ast[k] = {
            'type': REMOVED,
            'path': f'{path}{k}',
            'value': file1[k]
        }
    for k in file2:
        if k not in file1:
            if isinstance(file2[k], dict):
                ast[k] = {
                    'type': ADDED,
                    'path': f'{path}{k}',
                    'children': build_nested(file2[k])
                }
            else:
                ast[k] = {
                    'type': ADDED,
                    'path': f'{path}{k}',
                    'value': file2[k]
                }
    return ast
