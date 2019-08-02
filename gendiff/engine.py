import json
import yaml
import os.path
from gendiff.formatters import string, plain, m_json


UNSUPPORTED_FORMATS = 'unsupported_formats'
DIFFERENT_FORMATS = 'different_formats'

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


# def get_json_files(first_file, second_file):
#     with open(first_file, "r") as src_file1:
#         file1 = json.load(src_file1)
#     with open(second_file, "r") as src_file2:
#         file2 = json.load(src_file2)
#     return (file1, file2)


BLANKS = {
    FORMAT_STRING: lambda: '{\n',
    FORMAT_PLAIN: lambda: [],
    FORMAT_JSON: lambda: {}
}


# FILE_OPEN_TOOLS = {
#     '.yml': get_yml_files,
#     '.json': get_json_files
# }


def get_error_message(file_name=None, file_format=None):
    # if message_type == UNSUPPORTED_FORMATS:
    return (
        f'The format of {file_name} "{file_format}" '
        'is not supported by this program. '
        'Try to compare "json" or "yml" formats.'
    )
    # if message_type == DIFFERENT_FORMATS:
    #     return (
    #         'Files have different formats. '
    #         'Try to compare same formats'
    #     )


def get_diff(first_file, second_file, format):
    format = FORMAT_STRING if format is None else format
    first_file_format = os.path.splitext(first_file)[-1]
    second_file_format = os.path.splitext(second_file)[-1]
    if (first_file_format != '.json' and first_file_format != '.yml'):
        message = get_error_message(
            # UNSUPPORTED_FORMATS,
            first_file,
            first_file_format
        )
        return print(message)
    if (second_file_format != '.json' and second_file_format != '.yml'):
        message = get_error_message(
            # UNSUPPORTED_FORMATS,
            second_file,
            second_file_format
        )
        return print(message)
    # if (first_file_format != second_file_format):
    #     message = get_error_message(DIFFERENT_FORMATS)
    #     return print(message)
    # get_files_value = switch_case(first_file_format, FILE_OPEN_TOOLS)
    file1 = get_file(first_file_format, first_file)
    file2 = get_file(second_file_format, second_file)
    result = build_by_pieces(format, file1, file2)
    if format == FORMAT_JSON:
        result = json.dumps(result)
    if format == FORMAT_PLAIN:
        result = '\n'.join(result)
    return result


def build_element(format, *args):
    builder = BUILDERS_FORMATS[format]
    # if format == FORMAT_STRING:
    return builder.build_element(args)
    # if format == FORMAT_PLAIN:
    #     return builder.build_element(container, key, element, operator, path)
    # if format == FORMAT_JSON:
    #     return builder.build_element(container, key, element, operator)


def build_nested(node, indent, format):
    if format == FORMAT_PLAIN:
        return 'complex value'
    container = BLANKS[format]()
    for k in node:
        if type(node[k]) is dict:
            nested_element = build_nested(node[k], f'{indent}    ', format)
            container = build_element(
                format,
                container,
                k,
                nested_element,
                f'{indent}    ',
                '  ',
                None
            )
    else:
        container = build_element(
            format, container, k, node[k], f'{indent}', '  ', None
        )
    if format == FORMAT_STRING:
        container += indent + '}'
    return container


def build_by_pieces(format, file1, file2, indent='', path=''):
    container = BLANKS[format]()
    if not file1 and not file2:
        print('No data to compare, the files are empty')
        return
    for k in file1:
        if k in file1 and k in file2:
            if type(file1[k]) is dict and type(file1[k]) is dict:
                nested_diff = build_by_pieces(
                    format,
                    file1[k],
                    file2[k],
                    f'{indent}    ',
                    f'{path}{k}.'
                )
                container = build_element(
                    format, container, k, nested_diff, indent, '  ', path
                )
            elif file1[k] == file2[k]:
                container = build_element(
                    format, container, k, file1[k], indent, '  ', path
                )
            else:
                container = build_element(
                    format,
                    container,
                    k,
                    (file1[k], file2[k]),
                    indent,
                    '- ',
                    path
                )
        elif k in file1:
            if type(file1[k]) is dict:
                nested_element = build_nested(
                    file1[k],
                    f'{indent}    ',
                    format
                )
                container = build_element(
                    format, container, k, nested_element, indent, '- ', path
                )
            else:
                container = build_element(
                    format, container, k, file1[k], indent, '- ', path
                )
    for k in file2:
        if k not in file1:
            if type(file2[k]) is dict:
                nested_element = build_nested(
                    file2[k],
                    f'{indent}    ',
                    format
                )
                container = build_element(
                    format, container, k, nested_element, indent, '+ ', path
                )
            else:
                container = build_element(
                    format, container, k, file2[k], indent, '+ ', path
                )
    if format == FORMAT_STRING:
        container += indent + '}'
    return container
