import json
import yaml
import os.path
from gendiff.formatters import string, plain
import gendiff.formatters.json as formatters_json
from gendiff.diff_getter.ast_builder import build_ast


JSON_EXTENSIONS = ('.json',)
YAML_EXTENSIONS = ('.yml', '.yaml')
VALID_EXTENSIONS = JSON_EXTENSIONS + YAML_EXTENSIONS

FORMAT_STRING, FORMAT_PLAIN, FORMAT_JSON = ('string', 'plain', 'json')

BUILDERS_FORMATS = {
    FORMAT_STRING: string,
    FORMAT_PLAIN: plain,
    FORMAT_JSON: formatters_json
}


def get_file_content(file_path):
    file_extension = os.path.splitext(file_path)[-1]
    if file_extension not in VALID_EXTENSIONS:
        message = get_error_message(
            file_path,
            file_extension
        )
        return print(message)
    if file_extension in JSON_EXTENSIONS:
        with open(file_path, "r") as src_file:
            file_content = json.load(src_file)
    if file_extension in YAML_EXTENSIONS:
        with open(file_path, "r") as src_file:
            file_content = yaml.load(src_file, yaml.Loader)
    return file_content


def get_error_message(file_name, file_extension):
    return (
        f'The format of {file_name} "{file_extension}" '
        'is not supported by this program. '
        'Try to compare "json" or "yml" formats.'
    )


def build_representation(format, ast):
    builder = BUILDERS_FORMATS[format]
    return builder.build_representation(ast)


def get_diff(old_file, new_file, format):
    format = format or FORMAT_STRING
    old_file_content = get_file_content(old_file)
    new_file_content = get_file_content(new_file)
    if not old_file_content or not new_file_content:
        print('pass')
        return
    ast = build_ast(old_file_content, new_file_content)
    result = build_representation(format, ast)
    return result
