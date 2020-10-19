import unittest

from filters import Filters
from tests.data import data

class TestFilters(unittest.TestCase):
    def setUp(self):
        self.filters = Filters(None)

    def test_filter_data_equal(self):
        filtered = self.filters.filter_data(data, 'name', '=', 'John Doe')

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['name'], 'John Doe')

    def test_filter_data_not_equal(self):
        filtered = self.filters.filter_data(data, 'name', '!=', 'John Doe')

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['name'], 'Marie Freeman')
        self.assertEqual(filtered[1]['name'], 'Lisa Smith')

    def test_filter_data_is_contained(self):
        filtered = self.filters.filter_data(data, 'favourite_foods.name', '~>', 'Lemon Pie, Chocolate Cake')

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['name'], 'John Doe')
        self.assertEqual(filtered[1]['name'], 'Lisa Smith')

    def test_filter_data_contains(self):
        filtered = self.filters.filter_data(data, 'address.city', '<~', 'Garden')

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['name'], 'Marie Freeman')
        self.assertEqual(filtered[1]['name'], 'Lisa Smith')

    def test_filter_data_greater_than(self):
        filtered = self.filters.filter_data(data, 'age', '>', '40')

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['name'], 'John Doe')

    def test_filter_data_greater_than_or_equal_to(self):
        filtered = self.filters.filter_data(data, 'age', '>=', '35')

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['name'], 'John Doe')
        self.assertEqual(filtered[1]['name'], 'Lisa Smith')

    def test_filter_data_less_than(self):
        filtered = self.filters.filter_data(data, 'age', '<', '34')

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['name'], 'Marie Freeman')

    def test_filter_data_less_than_or_equal_to(self):
        filtered = self.filters.filter_data(data, 'age', '<=', '35')

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['name'], 'Marie Freeman')
        self.assertEqual(filtered[1]['name'], 'Lisa Smith')

    def test_filter_data_invalid_operator(self):
        with self.assertRaises(Exception) as err:
            filtered = self.filters.filter_data(data, 'age', '*+', '35')

        self.assertEqual(str(err.exception), 'Unknown operator \'*+\'')

    def test_filter_data_not_a_list(self):
        filtered = self.filters.filter_data('not a list', 'age', '>=', '35')

        self.assertEqual(filtered, 'not a list')

    def test_filter_data_field_not_found(self):
        filtered = self.filters.filter_data(data, 'old', '=', '35')

        self.assertEqual(len(filtered), 0)

    def test_filter_data_invalid_number(self):
        filtered = self.filters.filter_data(data, 'age', '>', 'five')

        self.assertEqual(len(filtered), 0)

if __name__ == '__main__':
    unittest.main()
