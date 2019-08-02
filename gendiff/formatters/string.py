def build_element(args):
    # format, container, k, nested_diff, indent, '  ', path
    container, key, element, indent, operator, path = args
    if type(element) == tuple:
        (old_value, new_value) = element
        container += f'{indent}  - {key}: {old_value}\n'
        container += f'{indent}  + {key}: {new_value}\n'
        return container
    return f'{container}{indent}  {operator}{key}: {element}\n'
