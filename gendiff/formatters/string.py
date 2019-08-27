from gendiff.constants import UNCHANGED, CHANGED, ADDED, REMOVED
import json

_OPERATORS = {
    UNCHANGED: ' ',
    REMOVED: '-',
    ADDED: '+'
}


def build_representation(ast, indent=''):
    print(f'ast is {ast}\n')
    result = ['{']
    for k, v in ast.items():
        result.extend(build_element(k, v, indent))
    result.append(f'{indent}}}')
    return '\n'.join(result)


def build_element(key, node, indent=''):
    result = []
    template = f'{indent}  {{0}} {key}: {{1}}'

    def add(*args):
        result.append(template.format(*args))
    node_type = node.get('type')
    if node_type == CHANGED:
        add("-", node['old_value'])
        add("+", node['new_value'])
    else:
        add(_OPERATORS[node_type], get_value(node, indent))
    return result


def get_value(node, indent):
    if node.get('children'):
        result = build_representation(node.get('children'), f'{indent}    ')
    elif node.get('value') and isinstance(node.get('value'), dict):
        result = build_unchanged_value(node.get('value'), f'{indent}    ')
    else:
        result = node.get('value')
    return result


def build_unchanged_value(element, indent):
    result = ['{']
    for k, v in element.items():
        if not isinstance(v, dict):
            result.append(f'{indent}    {k}: {v}')
        else:
            new_value = build_element(v, f'{indent}    ')
            result.append(new_value)
    result.append(f'{indent}}}')
    return '\n'.join(result)
