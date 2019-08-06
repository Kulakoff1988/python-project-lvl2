# from gendiff.constants import UNCHANGED, CHANGED, ADDED, REMOVED


def build_representation(ast):
    result = get_diff_list(ast)
    return '\n'.join(result)


def get_diff_list(ast):
    result = []
    for k in ast:
        result.extend(build_element(ast[k], k))
    return result


def build_element(element, key):
    result = []
    if element['type'] == UNCHANGED and element.get('children'):
        result.extend(get_diff_list(element.get('children')))
    path = element.get('path')
    if element['type'] == REMOVED:
        result.append(f'Property "{path}" was removed')
    if element['type'] == ADDED:
        value = element.get('value') if element.get('value') else 'complex value'
        result.append(
            f'Property "{path}" was added with value: "{value}"'
        )
    if element['type'] == CHANGED:
        result.append(
            f'Property "{path}" was changed. '
            f'From "{element["old_value"]}" to "{element["new_value"]}"'
        )
    return result
