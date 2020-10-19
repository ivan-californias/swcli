import re
import threading

from api import Api

class Filters:
    def __init__(self, api: Api):
        self._api = api

    def _parse_number(self, value):
        try:
            number = float(re.sub('[^.\-\d]', '', str(value)))
            return number
        except ValueError:
            return float('nan')

    def _get_property_values_append(self, item, props, values=[]):
        if type(item) is str and item.startswith('http'):
            new_data = self._api.do_request(item)
            values.append(self._get_property_value(new_data, props))
        else:
            values.append(self._get_property_value(item, props))

        return values

    def _get_property_value(self, data, props):
        if len(props) == 1:
            try:
                return data[props[0]]
            except:
                return ''

        if type(data[props[0]]) is not list:
            return self._get_property_value(data[props[0]], props[1:])

        values = []
        threads = []
        for item in data[props[0]]:
            th = threading.Thread(target=self._get_property_values_append, args=(item, props[1:], values))
            threads.append(th)
            th.start()
        for th in threads:
            th.join()
        return values

    def _compare_values(self, value_a, value_b, operator):
        if type(value_a) is list:
            for value in value_a:
                result = self._compare_values(value, value_b, operator)
                if result:
                    return True
            return False

        if operator == '=':
            return value_a == value_b
        if operator == '!=':
            return value_a != value_b
        if operator == '~>':
            return value_a in value_b
        if operator == '<~':
            return value_b in value_a

        num_a = self._parse_number(value_a)
        num_b = self._parse_number(value_b)
        if operator == '>':
            return num_a > num_b
        if operator == '<':
            return num_a < num_b
        if operator == '<=':
            return num_a <= num_b
        if operator == '>=':
            return num_a >= num_b

        raise Exception('Unknown operator \'%s\'' % operator)

    def filter_data(self, data, field_name, operator, value):
        if type(data) is not list:
            return data

        props = list(map(str.strip, field_name.split(sep='.')))
        filtered_data = []
        for item in data:
            cmp_value = self._get_property_value(item, props)
            if self._compare_values(cmp_value, value, operator):
                filtered_data.append(item)

        return filtered_data

