import swapi
import re

OPERATORS = ['=', '<~', '~>', '>', '<', '>=', '<=']

def _parse_number(value):
    try:
        number = float(re.sub('[^.\-\d]', '', value))
        return number
    except ValueError:
        return float('nan')

def _get_property_value(data, props):
    if len(props) == 1:
        try:
            return data[props[0]]
        except:
            return ''

    if type(data[props[0]]) is not list:
        return _get_property_value(data[props[0]], props[1:])

    values = []
    for item in data[props[0]]:
        if item.startswith('http'):
            new_data = swapi.call(item)
            values.append(_get_property_value(new_data, props[1:]))
        else:
            values.append(_get_property_value(item, props[1:]))
    return values

def _compare_values(value_a, value_b, operator):
    if type(value_a) is list:
        for value in value_a:
            result = _compare_values(value, value_b, operator)
            if result:
                return result
        return False

    if operator == '=':
        return value_a == value_b
    if operator == '~>':
        return value_a in value_b
    if operator == '<~':
        return value_b in value_a

    num_a = _parse_number(value_a)
    num_b = _parse_number(value_b)
    if operator == '>':
        return num_a > num_b
    if operator == '<':
        return num_a < num_b
    if operator == '<=':
        return num_a <= num_b
    if operator == '>=':
        return num_a >= num_b

    return False

def filter_data(data, filter=[]):
    if type(data) is not list or not filter:
        return data

    props = list(map(str.strip, filter[0].split(sep='.')))
    filtered_data = []
    for item in data:
        cmp_value = _get_property_value(item, props)
        if _compare_values(cmp_value, filter[2], filter[1]):
            filtered_data.append(item)

    return filtered_data

