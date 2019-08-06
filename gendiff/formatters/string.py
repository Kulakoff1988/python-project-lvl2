from gendiff.constants import UNCHANGED


def build_representation(ast, indent=''):
    result = ''
    for k in ast:
        result += build_element(ast[k], k, indent)
    return '{\n' + result + indent + '}'


def build_element(element, key, indent=''):
    if element.get('value'):
        value = element["value"]
    if element.get('children'):
        value = build_representation(element.get('children'), f'{indent}    ')
    if element['type'] == UNCHANGED:
        result = f'{indent}    {key}: {value}\n'
    if element['type'] == REMOVED:
        result = f'{indent}  - {key}: {value}\n'
    if element['type'] == ADDED:
        result = f'{indent}  + {key}: {value}\n'
    if element['type'] == CHANGED:
        result = f'{indent}  - {key}: {element["old_value"]}\n'
        result += f'{indent}  + {key}: {element["new_value"]}\n'
    return result
