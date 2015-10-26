import sys
import shutil
import brewpiJson
import time
import json
from BrewPiUtil import logMessage

class DataLogger(object):
    
    @classmethod
    def setFiles(self, localJsonFileName, wwwJsonFileName, localCsvFileName, wwwCsvFileName):
        self.localJsonFileName = localJsonFileName
        self.wwwJsonFileName = wwwJsonFileName
        self.localCsvFileName = localCsvFileName
        self.wwwCsvFileName = wwwCsvFileName
        
    @classmethod
    def printFiles(self):
        return self.localJsonFileName + '\n' + self.wwwJsonFileName + '\n' + self.localCsvFileName + '\n' + self.wwwCsvFileName

    @classmethod
    def renameTempKey(self, key):
        rename = {
            "bt": "BeerTemp",
            "bs": "BeerSet",
            "ba": "BeerAnn",
            "ft": "FridgeTemp",
            "fs": "FridgeSet",
            "fa": "FridgeAnn",
            "rt": "RoomTemp",
            "s": "State",
            "t": "Time"}
        return rename.get(key, key)

    @classmethod
    def renameAndCopyKeys(self, newData):
        prevTempJson = {
            "BeerTemp": 0,
            "FridgeTemp": 0,
            "BeerAnn": None,
            "FridgeAnn": None,
            "RoomTemp": None,
            "State": None,
            "BeerSet": 0,
            "FridgeSet": 0}
        
        for key in newData:
            prevTempJson[self.renameTempKey(key)] = newData[key]
        
        return prevTempJson

    @classmethod
    def jsonLog(self, newRow):
        # TODO: Extract
        brewpiJson.addRow(self.localJsonFileName, newRow)
        # copy to www dir.
        # Do not write directly to www dir to prevent blocking www file.
        shutil.copyfile(self.localJsonFileName, self.wwwJsonFileName)

    @classmethod
    def csvLog(self, newRow):
        # TODO: Extract 
        csvFile = open(self.localCsvFileName, "a")
        try:
            lineToWrite = (time.strftime("%b %d %Y %H:%M:%S;") + json.dumps(newRow['BeerTemp']) + ';' + json.dumps(newRow['BeerSet']) + ';' + json.dumps(newRow['BeerAnn']) + ';' + json.dumps(newRow['FridgeTemp']) + ';' + json.dumps(newRow['FridgeSet']) + ';' + json.dumps(newRow['FridgeAnn']) + ';' + json.dumps(newRow['State']) + ';' + json.dumps(newRow['RoomTemp']) + '\n')
            csvFile.write(lineToWrite)
        except KeyError, e:
            logMessage("KeyError in line from controller: %s" % str(e))
        
        csvFile.close()
        shutil.copyfile(self.localCsvFileName, self.wwwCsvFileName)

    @classmethod
    def datalogJsonCsvAndCopy(self, newData):
        newRow = self.renameAndCopyKeys(newData)
        self.jsonLog(newRow)
        self.csvLog(newRow)
