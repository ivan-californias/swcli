import unittest

from filters import Filters
from tests.data import data

class TestFilters(unittest.TestCase):

    def test_filter_data(self):
        filters = Filters(None)
        filtered = filters.filter_data(data, 'name', '=', 'John Doe')
        self.assertEqual(len(filtered), 1)

if __name__ == '__main__':
    unittest.main()
