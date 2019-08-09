from gendiff.constants import UNCHANGED, CHANGED, ADDED, REMOVED


def build_representation(ast):
    result = get_diff_list(ast)
    return '\n'.join(result)


def get_diff_list(ast):
    result = []
    for k, v in ast.items():
        result.extend(build_element(k, v))
    return result


def build_element(key, node):
    result = []
    node_type = node.get('type')
    if node_type == UNCHANGED and node.get('children'):
        result.extend(get_diff_list(node.get('children')))
    if node_type != UNCHANGED:
        path = '.'.join(node.get('path'))
    if node_type == REMOVED:
        result.append(f'Property "{path}" was removed')
    elif node_type == ADDED:
        value = get_value(node)
        result.append(
            f'Property "{path}" was added with value: "{value}"'
        )
    elif node_type == CHANGED:
        result.append(
            f'Property "{path}" was changed. '
            f'From "{node.get("old_value")}" to "{node.get("new_value")}"'
        )
    return result


def get_value(node):
    if not isinstance(node.get('value'), dict):
        value = node.get('value')
    else:
        value = 'complex value'
    return value
