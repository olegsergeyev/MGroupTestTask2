import unittest
import datetime
from unittest.mock import patch
from median.percentile import calculate_percentiles
from median.client_socket import process_message

class TestPercetile(unittest.TestCase):
    def test_result(self):
        values = [2, 6, 13, 13, 8, 9, 0, 11, 17, 11, 15, 3, 5, 9, 15, 4, 19, 3, 8, 8, 8, 3, 13, 7, 14, 4, 20, 19, 6, 2,
                  8, 11, 17, 11, 14, 6, 18, 5, 9, 0, 13, 16, 17, 2, 16, 12, 12, 8, 17, 10, 17, 15, 18, 12, 6, 9, 3, 12,
                  3, 13, 9, 3, 20, 7, 14, 8, 6, 17, 11, 2, 12, 1, 18, 14, 19, 19, 11, 0, 10, 13, 14, 17, 14, 20, 3, 9,
                  9, 9, 4, 7, 11, 7, 2, 16, 6, 11, 17, 1, 16]
        delta = 1
        p25 = median = p75 = 0
        for value in values:
            p25, median, p75 = calculate_percentiles(delta, value, p25, median, p75)
        self.assertLessEqual((p25 - 6), delta)
        self.assertLessEqual((median - 11), delta)
        self.assertLessEqual((p75 - 15), delta)

    @patch('median.client_socket.create_record')
    def test_process_message(self, create_record_mk):
        message = '2020-02-23 22:09:07.841161_0'
        last_record = datetime.datetime.strptime('2020-02-23 22:00:07.841161', '%Y-%m-%d %H:%M:%S.%f')
        process_message(message, 1, last_record, 0, 0, 0)
        create_record_mk.assert_called_with(datetime.datetime(2020, 2, 23, 22, 9, 7, 841161), -0.5, 0.0, 0.5)


if __name__ == '__main__':
    unittest.main()
