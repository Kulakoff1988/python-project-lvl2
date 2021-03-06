from gendiff.constants import UNCHANGED, CHANGED, ADDED, REMOVED
import json


def build_ast(old_file, new_file, path=()):
    ast = {}
    build_ast_from_old_file(old_file, new_file, ast, path)
    build_ast_from_new_file(old_file, new_file, ast, path)
    return ast


def build_ast_from_old_file(old_file, new_file, container_ast, path):
    for k, v in old_file.items():
        new_path = path + (k,)
        if k in new_file:
            new_value = new_file.get(k)
            if isinstance(v, dict) and isinstance(new_value, dict):
                content = {
                    'type': UNCHANGED,
                    'children': build_ast(v, new_value, new_path)
                }
            elif v == new_value:
                content = {
                    'type': UNCHANGED,
                    'value': v
                }
            elif v != new_value:
                content = {
                    'type': CHANGED,
                    'path': new_path,
                    'old_value': v,
                    'new_value': new_value
                }
        else:
            content = {
                'type': REMOVED,
                'path': new_path,
                'value': v
            }
        container_ast[k] = content


def build_ast_from_new_file(old_file, new_file, container_ast, path):
    for k, v in new_file.items():
        if k not in old_file:
            new_path = path + (k,)
            content = {
                'type': ADDED,
                'path': new_path,
                'value': v
            }
            container_ast[k] = content
