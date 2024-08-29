from includes.DataFile import DataFile


###################################
# CallData class
###################################
class CallData(DataFile):
    # Data File to load
    @property
    def data_file(self):
        return super().data_file.lower()

    # Type of the data file (CSV | JSON)
    @property
    def file_type(self):
        _file_type = super().file_type.lower()
        return _file_type

    #
    # Methods

