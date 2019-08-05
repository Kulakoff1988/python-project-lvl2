def build_representation(args):
    container, key, element, indent, operator, path = args
    if type(element) == tuple:
        (old_value, new_value) = element
        container[f'- {key}'] = old_value
        container[f'+ {key}'] = new_value
        return container
    operator = '' if operator == '  ' else operator
    container[operator + key] = element
    return container
