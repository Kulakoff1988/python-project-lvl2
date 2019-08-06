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


def build_ast(file1, file2, path=''):
    ast = {}
    if not file1 and not file2:
        print('No data to compare, the files are empty')
        return
    for k in file1:
        if k in file2:
            if isinstance(file1[k], dict) and isinstance(file2[k], dict):
                ast[k] = {
                    'type': UNCHANGED,
                    'children': build_ast(file1[k], file2[k], f'{path}{k}.')
                }
                continue
            if file1[k] == file2[k]:
                ast[k] = {
                    'type': UNCHANGED,
                    'value': file1[k]
                }
                continue
            if file1[k] != file2[k]:
                ast[k] = {
                    'type': CHANGED,
                    'path': f'{path}{k}',
                    'old_value': file1[k],
                    'new_value': file2[k]
                }
                continue
        if isinstance(file1[k], dict):
            ast[k] = {
                'type': REMOVED,
                'path': f'{path}{k}',
                'children': build_nested(file1[k])
            }
            continue
        ast[k] = {
            'type': REMOVED,
            'path': f'{path}{k}',
            'value': file1[k]
        }
    for k in file2:
        if k not in file1:
            if isinstance(file2[k], dict):
                ast[k] = {
                    'type': ADDED,
                    'path': f'{path}{k}',
                    'children': build_nested(file2[k])
                }
            else:
                ast[k] = {
                    'type': ADDED,
                    'path': f'{path}{k}',
                    'value': file2[k]
                }
    return ast
