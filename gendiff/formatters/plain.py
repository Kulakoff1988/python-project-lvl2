def get_diff(result, key, element, operator, path):
    if type(element) == tuple:
        (old_value, new_value) = element
        result.append(
            f'Property "{path}{key}" was changed. '
            f'From "{old_value}" to "{new_value}"'
        )
    if operator == '+ ':
        result.append(
            f'Property "{path}{key}" was added with value: "{element}"'
        )
    if operator == '- ' and type(element) != tuple:
        result.append(f'Property "{path}{key}" was removed')
    return result
