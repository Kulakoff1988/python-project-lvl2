import json
import yaml
import os.path
from gendiff.constants import *


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
    print(result)
    if format == FORMAT_JSON:
        result = json.dumps(result)
    if format == FORMAT_PLAIN:
        result = '\n'.join(result)
    return result


def build_representation(format, ast):
    builder = BUILDERS_FORMATS[format]
    return builder.build_representation(ast)


def build_nested(node, parent):
    print(f'node is {node}')
    ast = {}
    for k in node:
        ast[k] = {
            'complex_value': True
        }
        if type(node[k]) is dict:
            nested_element = build_nested(node[k], k)
            ast[k].update({
                    'type': 'unchange',
                    'parent': k,
                    'children': nested_element
                })
        else:
            ast[k].update({
                    'value': node[k],
                    'type': 'unchange',
                })
    return ast


def build_ast(file1, file2):
    ast = {}
    if not file1 and not file2:
        print('No data to compare, the files are empty')
        return
    for k in file1:
        if k not in file2:
            if type(file1[k]) is dict:
                print(f'value is {file1[k]} {k}')
                nested_ast = build_ast(file1[k], k)
                ast[k] = {
                    'type': 'nested',
                    'parent': k,
                    'children': nested_ast
                }
                continue
            ast[k] = {
                'type': 'removed',
                'value': file1[k]
            }
        if isinstance(file1[k], dict) and isinstance(file2[k], dict):
            ast[k] = {
                'type': 'nested',
                'parent': k,
                'children': build_ast(file1[k], file2[k])
            }
            continue
        if file1[k] != file2[k]:
            ast[k] = {
                'type': 'changed',
                'old_value': file1[k],
                'new_value': file2[k] 
            }
            continue
        ast[k] = {
            'type': 'unchange',
            'value': file1[k]
        }
    for k in file2:
        if k not in file1:
            if isinstance(file2[k], dict):
                print(f'value is {file2[k]} {k}')
                nested_ast = build_nested(file2[k], k)
                ast[k] = {
                    'type': 'nested',
                    'parent': k,
                    'children': nested_ast
                }
            else:
                ast[k] = {
                    'type': 'added',
                    'value': file2[k],
                } 
    print(json.dumps(ast, indent=2))
    return ast
