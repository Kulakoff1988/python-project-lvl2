from gendiff.constants import UNCHANGED, CHANGED, ADDED, REMOVED


def build_representation(ast, indent=''):
    result = ['{']
    for k, v in ast.items():
        result.extend(build_element(k, v, indent))
    result.append(f'{indent}}}')
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
        add("-", node.get('old_value'))
        add("+", node.get('new_value'))
    else:
        add(_OPERATORS[node_type], get_value(node, indent))
    return result


def get_value(node, indent):
    if node.get('value'):
        result = node.get('value')
    else:
        result = build_representation(node.get('children'), f'{indent}    ')
    return result
