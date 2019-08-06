import json
import yaml
import os.path
from gendiff.formatters import string, plain, m_json
from gendiff.diff_getter.ast_builder import build_ast


JSON_FORMAT = '.json'
YAML_FORMAT = '.yml'

FORMAT_STRING, FORMAT_PLAIN, FORMAT_JSON = ('string', 'plain', 'json')

BUILDERS_FORMATS = {
    FORMAT_STRING: string,
    FORMAT_PLAIN: plain,
    FORMAT_JSON: m_json
}


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


def build_representation(format, ast):
    builder = BUILDERS_FORMATS[format]
    return builder.build_representation(ast)


def get_diff(first_file, second_file, format):
    format = FORMAT_STRING if format is None else format
    first_file_format = os.path.splitext(first_file)[-1]
    second_file_format = os.path.splitext(second_file)[-1]
    if (first_file_format != JSON_FORMAT and first_file_format != YAML_FORMAT):
        message = get_error_message(
            first_file,
            first_file_format
        )
        return print(message)
    if (second_file_format != JSON_FORMAT and second_file_format != YAML_FORMAT):
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
