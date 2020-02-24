import unittest
import pandas as pd
from matrix.sort_matrix import generate, fast_sort_matrix


class SortMatrix(unittest.TestCase):
    def test_generate(self):
        generate('test.csv', 4, 5)
        matrix = pd.read_csv(filepath_or_buffer='test.csv', sep=' ', header=None)
        self.assertEqual(matrix.shape, (4, 5))

    def test_result(self):
        values = pd.DataFrame([[0, 5, 6, 8, 2], [1, 4, 7, 1, 5], [0, 6, 8, 5, 3]])
        values.to_csv(path_or_buf='test.csv', sep=' ', mode='w', header=False, index=False)
        fast_sort_matrix('test.csv', 'sorted_test.csv')
        result = pd.read_csv(filepath_or_buffer='sorted_test.csv', sep=' ', header=None)
        sorted_values = pd.DataFrame([[0, 4, 6, 1, 2], [0, 5, 7, 5, 3], [1, 6, 8, 8, 5]])
        self.assertTrue(result.equals(sorted_values))


if __name__ == '__main__':
    unittest.main()
