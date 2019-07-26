def build_element(container, key, element, indent, operator):
    if type(element) == tuple:
        (old_value, new_value) = element
        container += f'{indent}  - {key}: {old_value}\n'
        container += f'{indent}  + {key}: {new_value}\n'
        return container
    return f'{container}{indent}  {operator}{key}: {element}\n'
