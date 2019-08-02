def build_element(args):
    # def build_element(container, key, element, operator, path):
    container, key, element, indent, operator, path = args
    if type(element) is tuple:
        (old_value, new_value) = element
        container.append(
            f'Property "{path}{key}" was changed. '
            f'From "{old_value}" to "{new_value}"'
        )
    if operator == '+ ':
        container.append(
            f'Property "{path}{key}" was added with value: "{element}"'
        )
    if operator == '- ' and type(element) is not tuple:
        container.append(f'Property "{path}{key}" was removed')
    if type(element) is list:
        container.extend(element)
    return container
