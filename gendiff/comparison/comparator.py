import json
import yaml


def get_diff(first_file, second_file, format=None):
    first_file_format = first_file.split('.')[-1]
    second_file_format = second_file.split('.')[-1]
    if (first_file_format != 'json' and first_file_format != 'yml'):
        print(
            f'The format of {first_file} "{first_file_format}" '
            'is not supported by this program. '
            'Try to compare "json" or "yml" formats.'
        )
        return
    if (second_file_format != 'json' and second_file_format != 'yml'):
        print(
            f'The "{second_file_format}" format '
            'is not supported by this program. '
            'Try to compare "json" or "yml" formats.'
        )
        return
    if (first_file_format != second_file_format):
        print(
            'Files have different formats. '
            'Try to compare same formats'
        )
        return
    if (first_file_format == 'json'):
        (file1, file2) = get_json_files(first_file, second_file)
    if (first_file_format == 'yml'):
        (file1, file2) = get_yml_files(first_file, second_file)
    result = run_diff(file1, file2, '', format)
    if format == 'json':
        return result
    print(result)
    return result


def get_yml_files(first_file, second_file):
    file1 = yaml.load(open(first_file), yaml.Loader)
    file2 = yaml.load(open(second_file), yaml.Loader)
    return (file1, file2)


def get_json_files(first_file, second_file):
    file1 = json.load(open(first_file))
    file2 = json.load(open(second_file))
    return (file1, file2)


def add_children(node, indent, format):
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
        print('pass')
        return json.dumps(json_result)
    return result + indent + '}'


def run_diff(file1, file2, indent, format=None, path=''):
    result = '{\n'
    plain_result = []
    json_result = {}
    if not file1 and not file2:
        print('No data to compare, the files are empty')
        return
    for k in file1:
        if k in file1 and k in file2:
            if type(file1[k]) is dict and type(file1[k]) is dict:
                diff_branch = run_diff(
                    file1[k],
                    file2[k],
                    f'{indent}    ',
                    format,
                    f'{path}{k}.'
                )
                result += f'    {indent}{k}: {diff_branch}\n'
                json_result[f' {k}'] = diff_branch
                plain_result.append(diff_branch)
            elif file1[k] == file2[k]:
                result += f'    {indent}{k}: {file1[k]}\n'
                json_result[f'{k}'] = file1[k]
            else:
                result += f'  {indent}- {k}: {file1[k]}\n'
                result += f'  {indent}+ {k}: {file2[k]}\n'
                plain_result.append(
                    f'Property "{path}{k}" was changed.'
                    f'From "{file1[k]}" to "{file2[k]}"'
                )
                json_result[f'- {k}'] = file1[k]
                json_result[f'+ {k}'] = file2[k]
        elif k in file1:
            if type(file1[k]) is dict:
                child_branch = add_children(file1[k], f'{indent}    ', format)
                result += f'  {indent}- {k}: {child_branch}\n'
                plain_result.append(f'Property "{path}{k}" was removed')
                json_result[f'- {k}'] = child_branch
            else:
                result += f'  {indent}- {k}: {file1[k]}\n'
                plain_result.append(f'Property "{path}{k}" was removed')
                json_result[f'- {k}'] = file1[k]
    for k in file2:
        if k not in file1:
            if type(file2[k]) is dict:
                child_branch = add_children(file2[k], f'{indent}    ', format)
                result += f'  {indent}+ {k}: {child_branch}\n'
                plain_result.append(
                    f'Property "{path}{k}"'
                    'was added with value: "complex value"'
                )
            else:
                result += f'  {indent}+ {k}: {file2[k]}\n'
                plain_result.append(
                    f'Property "{path}{k}" was added with value: "{file2[k]}"'
                )
                json_result[f'+ {k}'] = file2[k]
    if format == 'plain':
        return '\n'.join(plain_result)
    if format == 'json':
        return json.dumps(json_result)
    return result + indent + '}'
