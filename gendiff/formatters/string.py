def get_diff(result, key, element, operator, indent):
    if type(element) == tuple:
        (old_value, new_value) = element
        result += f'{indent}  - {key}: {old_value}\n'
        result += f'{indent}  + {key}: {new_value}\n'
        return result
    return f'{result}{indent}  {operator}{key}: {element}\n'
