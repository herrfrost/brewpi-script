import unittest
import datetime
from testfixtures import Replacer
from datalogging import datalogger


class DataLoggerTestCase(unittest.TestCase):

    def setUp(self):
        self.log = datalogger.DataLogger()

    def test_update_data_keys(self):
        newdata = {'t': 'Oct 26 2015 19:01:47',
                   'bt': 22.31,
                   'bs': 'null',
                   'ba': 'null',
                   'ft': 22.53,
                   'fs': 'null',
                   'fa': 'null',
                   's': 0}

        result = self.log.update_data_keys(newdata)

        expected = {'BeerAnn': 'null',
                    'BeerSet': 'null',
                    'BeerTemp': 22.31,
                    'FridgeAnn': 'null',
                    'FridgeSet': 'null',
                    'FridgeTemp': 22.53,
                    'RoomTemp': None,
                    'State': 0,
                    'Time': 'Oct 26 2015 19:01:47'}

        self.assertEqual(result, expected)

    def test_csv_datetime_has_correct_format(self):
        with Replacer() as rep:
            rep.replace('datalogging.datalogger.time',
                        datetime.datetime(2015, 10, 26, 21, 27, 05))

            expected = 'Oct 26 2015 21:27:05;'
            result = self.log.get_csv_datetime()

            self.assertEqual(result, expected)

    def test_get_csvline_hascorrectformat(self):
        with Replacer() as rep:
            rep.replace('datalogging.datalogger.time',
                        datetime.datetime(2015, 10, 26, 21, 27, 05))

            newrow = {'BeerAnn': 'null',
                      'BeerSet': 'null',
                      'BeerTemp': 22.31,
                      'FridgeAnn': 'null',
                      'FridgeSet': 'null',
                      'FridgeTemp': 22.53,
                      'RoomTemp': None,
                      'State': 0,
                      'Time': 'Oct 26 2015 21:27:05'}

            result = self.log.get_csvline(newrow)
            expected = 'Oct 26 2015 21:27:05;22.31;"null"' + \
                       ';\"null";22.53;"null";"null";0;null\n'

            self.assertEqual(result, expected)

    def tearDown(self):
        self.log = None


if __name__ == '__main__':
    unittest.main()
