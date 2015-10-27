import shutil
import brewpiJson
import time
import json
from BrewPiUtil import logMessage


class DataLogger(object):
    @classmethod
    def get_csv_datetime(cls):
        return time.strftime("%b %d %Y %H:%M:%S;")

    def set_files(self, local_json_filename,
                  www_json_filename, local_csv_filename,
                  www_csv_filename):
        self.local_json_filename = local_json_filename
        self.www_jsonfilename = www_json_filename
        self.local_csv_filename = local_csv_filename
        self.www_csv_filename = www_csv_filename

    @staticmethod
    def rename_key(key):
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

    def update_data_keys(self, newdata):
        prevtempjson = {'BeerTemp': 0, 'FridgeTemp': 0,
                        'BeerAnn': None, 'FridgeAnn': None,
                        'RoomTemp': None, 'State': None,
                        'BeerSet': 0, 'FridgeSet': 0}

        for key in newdata:
            prevtempjson[self.rename_key(key)] = newdata[key]

        return prevtempjson

    def write_to_jsonlog(self, newrow):
        brewpiJson.addRow(self.local_json_filename, newrow)
        # copy to www dir.
        # Do not write directly to www dir to prevent blocking www file.
        shutil.copyfile(self.local_json_filename, self.www_jsonfilename)

    def get_csvline(self, newrow):
        linetowrite = (self.get_csv_datetime() +
                       json.dumps(newrow['BeerTemp']) +
                       ';' + json.dumps(newrow['BeerSet']) +
                       ';' + json.dumps(newrow['BeerAnn']) +
                       ';' + json.dumps(newrow['FridgeTemp']) +
                       ';' + json.dumps(newrow['FridgeSet']) +
                       ';' + json.dumps(newrow['FridgeAnn']) +
                       ';' + json.dumps(newrow['State']) +
                       ';' + json.dumps(newrow['RoomTemp']) + '\n')
        return linetowrite

    def write_to_csv_file(self, newrow):
        csvfile = open(self.local_csv_filename, "a")
        try:
            linetowrite = self.get_csvline(newrow)
            csvfile.write(linetowrite)
        except KeyError, e:
            logMessage("KeyError in line from controller: %s" % str(e))

        csvfile.close()
        shutil.copyfile(self.local_csv_filename, self.www_csv_filename)

    def add_to_log(self, newdata):
        newrow = self.update_data_keys(newdata)
        self.write_to_jsonlog(newrow)
        self.write_to_csv_file(newrow)
