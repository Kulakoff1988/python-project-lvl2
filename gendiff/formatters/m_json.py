def get_diff(result, key, element, operator):
    if type(element) == tuple:
        (old_value, new_value) = element
        result[f'- {key}'] = old_value
        result[f'+ {key}'] = new_value
        return result
    operator = '' if operator == '  ' else operator
    result[operator + key] = element
    return result
