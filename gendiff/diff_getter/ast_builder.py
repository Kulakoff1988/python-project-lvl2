from gendiff.constants import UNCHANGED, CHANGED, ADDED, REMOVED


def build_nested(node):
    nested_ast = {}
    for k in node:
        value = build_nested(node[k]) if isinstance(node[k], dict) else node[k]
        nested_ast[k] = {
            'type': UNCHANGED,
            'value': value
        }
    return nested_ast


def build_ast(old_file, new_file, path=''):
    ast = {}
    if not old_file and not new_file:
        print('No data to compare, the files are empty')
        return
    build_ast_from_old_file(old_file, new_file, ast, path)
    build_ast_from_new_file(old_file, new_file, ast, path)
    return ast


def build_ast_from_old_file(old_file, new_file, container_ast, path):
    for k in old_file:
        if k in new_file:
            if isinstance(old_file[k], dict) and isinstance(new_file[k], dict):
                container_ast[k] = {
                    'type': UNCHANGED,
                    'children': build_ast(
                        old_file[k], new_file[k], f'{path}{k}.'
                    )
                }
                continue
            if old_file[k] == new_file[k]:
                container_ast[k] = {
                    'type': UNCHANGED,
                    'value': old_file[k]
                }
                continue
            if old_file[k] != new_file[k]:
                container_ast[k] = {
                    'type': CHANGED,
                    'path': f'{path}{k}',
                    'old_value': old_file[k],
                    'new_value': new_file[k]
                }
                continue
        if isinstance(old_file[k], dict):
            container_ast[k] = {
                'type': REMOVED,
                'path': f'{path}{k}',
                'children': build_nested(old_file[k])
            }
            continue
        container_ast[k] = {
            'type': REMOVED,
            'path': f'{path}{k}',
            'value': old_file[k]
        }


def build_ast_from_new_file(old_file, new_file, container_ast, path):
    for k in new_file:
        if k not in old_file:
            if isinstance(new_file[k], dict):
                container_ast[k] = {
                    'type': ADDED,
                    'path': f'{path}{k}',
                    'children': build_nested(new_file[k])
                }
            else:
                container_ast[k] = {
                    'type': ADDED,
                    'path': f'{path}{k}',
                    'value': new_file[k]
                }
