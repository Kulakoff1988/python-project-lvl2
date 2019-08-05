import json
def build_representation(ast, indent=''):
    # print(f'represent {ast}')
    result = ''
    for k in ast:
        result += build_element(ast[k], k, indent)
    return '{\n' + result + indent + '}'


def build_element(element, key, indent=''):
    if element['type'] == 'nested':
        nested_diff = build_representation(element.get('children'), '    ')
        result = f'{indent}    {key}: {nested_diff}\n'
    if element['type'] == 'unchange':
        result = f'{indent}    {key}: {element["value"]}\n'
    if element['type'] == 'removed':
        result = f'{indent}  - {key}: {element["value"]}\n'
    if element['type'] == 'added':
        result = f'{indent}  + {key}: {element["value"]}\n'
    if element['type'] == 'changed':
        result = f'{indent}  - {key}: {element["old_value"]}\n'
        result += f'{indent}  + {key}: {element["new_value"]}\n'
    return result
                