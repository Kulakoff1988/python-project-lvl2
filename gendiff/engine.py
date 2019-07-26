import json
import yaml
from gendiff.formatters import string, plain, m_json


def switch_case(case, dict):
    return dict.get(case, f'No case {case} in dictionary')


error_dict = {
    'unsupported_formats': lambda file_name, file_format: (
        f'The format of {file_name} "{file_format}" '
        'is not supported by this program. '
        'Try to compare "json" or "yml" formats.'
    ),
    'different_formats': lambda: (
        'Files have different formats. '
        'Try to compare same formats'
    )
}


container_dict = {
    'str': lambda: '{\n',
    'plain': lambda: [],
    'json': lambda: {}
}


file_open_tools = {
    'yml': lambda first_file, second_file: get_yml_files(
        first_file,
        second_file
    ),
    'json': lambda first_file, second_file: get_json_files(
        first_file,
        second_file
    )
}


def get_yml_files(first_file, second_file):
    with open(first_file, "r") as src_file1:
        file1 = yaml.load(src_file1, yaml.Loader)
    with open(second_file, "r") as src_file2:
        file2 = yaml.load(src_file2, yaml.Loader)
    return (file1, file2)


def get_json_files(first_file, second_file):
    with open(first_file, "r") as src_file1:
        file1 = json.load(src_file1)
    with open(second_file, "r") as src_file2:
        file2 = json.load(src_file2)
    return (file1, file2)


def get_diff(first_file, second_file, format='str'):
    first_file_format = first_file.split('.')[-1]
    second_file_format = second_file.split('.')[-1]
    if (first_file_format != 'json' and first_file_format != 'yml'):
        message = switch_case(
            'unsupported_formats',
            error_dict
        )(first_file, first_file_format)
        return print(message)
    if (second_file_format != 'json' and second_file_format != 'yml'):
        message = switch_case(
            'unsupported_formats',
            error_dict
        )(second_file, second_file_format)
        return print(message)
    if (first_file_format != second_file_format):
        message = switch_case('different_formats', error_dict)()
        return print(message)
    get_files_value = switch_case(first_file_format, file_open_tools)
    (file1, file2) = get_files_value(first_file, second_file)
    result = build_by_pieces(format, file1, file2)
    if format == 'json':
        result = json.dumps(result)
    if format == 'plain':
        result = '\n'.join(result)
    return result


def build_element(
    format,
    container,
    key,
    element,
    indent='',
    operator='',
    path=''
):
    if format == 'str':
        return string.build_element(container, key, element, indent, operator)
    if format == 'plain':
        return plain.build_element(container, key, element, operator, path)
    if format == 'json':
        return m_json.build_element(container, key, element, operator)


def build_nested(node, indent, format):
    if format == 'plain':
        return 'complex value'
    container = container_dict[format]()
    for k in node:
        if type(node[k]) is dict:
            nested_element = build_nested(node[k], f'{indent}    ', format)
            container = build_element(
                format, container, k, nested_element, f'{indent}    ', '  '
            )
    else:
        container = build_element(
            format, container, k, node[k], f'{indent}', '  '
        )
    if format == 'str':
        container += indent + '}'
    return container


def build_by_pieces(format, file1, file2, indent='', path=''):
    container = container_dict[format]()
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
    if format == 'str':
        container += indent + '}'
    return container
