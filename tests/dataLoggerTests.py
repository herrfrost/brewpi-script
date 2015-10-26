import unittest
from DataLogging import dataLogger

class DataLoggerTestCase(unittest.TestCase):

    def setUp(self):
        self.log = dataLogger.DataLogger()


    def test_setFilesSets(self):
        self.log.setFiles('localJsonFileName', 'wwwJsonFileName', 'localCsvFileName', 'wwwCsvFileName')
        
        result = self.log.printFiles()
        expected = 'localJsonFileName\nwwwJsonFileName\nlocalCsvFileName\nwwwCsvFileName'
        
        self.assertEqual(result, expected)

    def test_renameAndCopyKeys(self):
        newdata = {'t': 'Oct 26 2015 19:01:47', 'bt': 22.31, 'bs': 'null', 'ba': 'null', 'ft': 22.53, 'fs': 'null', 'fa': 'null', 's': 0}
        
        result = self.log.renameAndCopyKeys(newdata)
        expected = {'BeerAnn': 'null', 'BeerSet': 'null', 'BeerTemp': 22.31, 'FridgeAnn': 'null', 'FridgeSet': 'null', 'FridgeTemp': 22.53, 'RoomTemp': None, 'State': 0, 'Time': 'Oct 26 2015 19:01:47'}
        
        self.assertEqual(result, expected)


    def tearDown(self):
        self.log = None


if __name__ == '__main__':
    unittest.main()