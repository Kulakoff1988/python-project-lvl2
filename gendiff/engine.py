import json
import yaml
from gendiff.formatters import string, plain, m_json

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


def get_result(format, result, key, element, operator='', indent='', path=''):
    if format == 'str':
        return string.get_diff(result, key, element, operator, indent)
    if format == 'plain':
        return plain.get_diff(result, key, element, operator, path)
    if format == 'json':
        return m_json.get_diff(result, key, element, operator)


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
    if (first_file_format == 'json'):
        (file1, file2) = get_json_files(first_file, second_file)
    if (first_file_format == 'yml'):
        (file1, file2) = get_yml_files(first_file, second_file)
    result = run_diff(format, file1, file2)
    if format == 'json':
        return result
    return result


def switch_case(case, dict):
    return dict.get(case, f'No case {case} in dictionary')


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


def add_children(node, indent, format):
    if format == 'plain':
        return 'complex value'
    result = '{\n'
    json_result = {}
    for k in node:
        if type(node[k]) is dict:
            child_branch = add_children(node[k], f'{indent}    ', format)
            result += f'    {indent}{k}: {child_branch}\n'
            json_result[f'{k}'] = child_branch
    else:
        result += f'    {indent}{k}: {node[k]}\n'
        json_result[f'{k}'] = node[k]
    if format == 'json':
        return json.dumps(json_result)
    return result + indent + '}'


def run_diff(format, file1, file2, indent='', path=''):
    result_dict = {
        'str': '{\n',
        'plain': [],
        'json': {}
    }
    result = result_dict[format]
    if not file1 and not file2:
        print('No data to compare, the files are empty')
        return
    for k in file1:
        print(f'-1 {result}')
        if k in file1 and k in file2:
            print(f'0 {result}')
            if type(file1[k]) is dict and type(file1[k]) is dict:
                print(f'1 {result}')
                diff_branch = run_diff(
                    format,
                    file1[k],
                    file2[k],
                    f'{indent}    ',
                    f'{path}{k}.'
                )
                result = get_result(
                    format, result, k, diff_branch, '  ', indent, path
                )
            elif file1[k] == file2[k]:
                print(f'2 {result}')
                result = get_result(
                    format, result, k, file1[k], '  ', indent, path
                )
            else:
                print(f'3 {result}')
                result = get_result(
                    format, result, k, (file1[k], file2[k]), '- ', indent, path
                )
        elif k in file1:
            print(f'4 {result}')
            if type(file1[k]) is dict:
                print(f'5 {result}')
                child_branch = add_children(file1[k], f'{indent}    ', format)
                result = get_result(
                    format, result, k, child_branch, '- ', indent, path
                )
            else:
                print(f'6 {result}')
                result = get_result(
                    format, result, k, file1[k], '- ', indent, path
                )
    for k in file2:
        print(f'7 {result}')
        if k not in file1:
            print(f'8 {result}')
            if type(file2[k]) is dict:
                print(f'9 {result}')
                child_branch = add_children(file2[k], f'{indent}    ', format)
                result = get_result(
                    format, result, k, child_branch, '+ ', indent, path
                )
                print(f'10 {result}')
            else:
                print(f'11 {result}')
                result = get_result(
                    format, result, k, file2[k], '+ ', indent, path
                )
    if format == 'plain':
        return '\n'.join(result)
    if format == 'json':
        return json.dumps(result)
    return result + indent + '}'
