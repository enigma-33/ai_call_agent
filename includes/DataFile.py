import os
import json
import pandas as pd

###################################
# DataFile class
###################################
class DataFile:
    _data_file = None
    _default_data_file = None
    _file_extension = None
    _is_loaded = False
    _data = None
    #_file_type = None

    # Initializer
    def __init__(self, data_file):
        self._data_file = data_file
        
        # extract the file name and extension
        split_tup = os.path.splitext(self._data_file)
        self._file_name = split_tup[0]
        self._file_extension = split_tup[1]
 
    # Data File to load
    @property
    def data_file(self):
        return self._data_file

    @data_file.setter
    def data_file(self, value):
        self._data_file = value

    # Type of the data file
    @property
    def file_extension(self):
        return self._file_extension

    @file_extension.setter
    def file_extension(self, value):
        self._file_extension = value

    @property
    def file_type(self):
        return self.file_extension[1::]

    @property
    def is_loaded(self):
        return self._is_loaded
    #
    # Methods
    #
        
    # _load_csv(self):
    def load(self):
        try:
            if self.file_type == "csv":
                data = self._load_csv()
            elif self.file_type == "json":
                data = self._load_json()
            else:
                data = None
            self._data = data
            self._isLoaded = True
            return data

        except Exception as e:
            print(e)
            self._isLoaded = False
            return None
    
    # _load_csv(self):
    def _load_csv(self):
        try:
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(self.data_file)

            # Convert the DataFrame to a JSON object
            # _data_str = df.to_json(orient='records')
            data_json = df.to_json(orient='records')
            data = json.loads(data_json)

            return data

        except Exception as e:
            print(e)
            return None
        
    # _load_json(self):
    def _load_json(self):
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
            f.close()
            return data
        except Exception as e:
            print(e)
            return None

