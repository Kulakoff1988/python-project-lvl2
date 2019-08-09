from gendiff.constants import UNCHANGED, CHANGED, ADDED, REMOVED
import json


def build_representation(ast, indent=''):
    # print(f'ast is {json.dumps(ast, indent=2)}')
    result = ['{']
    for k, v in ast.items():
        result.extend(build_element(k, v, indent))
    result.append(f'{indent}}}')
    print(f'result is {result}')
    return '\n'.join(result)


_OPERATORS = {
    UNCHANGED: ' ',
    REMOVED: '-',
    ADDED: '+'
}


def build_element(key, node, indent=''):
    result = []
    template = f'{indent}  {{0}} {key}: {{1}}'

    def add(*args):
        result.append(template.format(*args))
    node_type = node.get('type')
    if node_type == CHANGED:
        add("-", node['old_value'])
        add("+", node['old_value'])
    else:
        add(_OPERATORS[node_type], get_value(node, indent))
    return result


def get_value(node, indent):
    # print(f'node is {node}')
    if node.get('children'):
        result = build_representation(node.get('children'), f'{indent}    ')
    elif node.get('value') and isinstance(node.get('value'), dict):
        result = get_value(node.get('value'), indent)
    else:
        result = node.get('value')
    return result