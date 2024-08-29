from includes.DataFile import DataFile


###################################
# AppConfig class
###################################
class AppConfig(DataFile):
    _auth_key = None

    # Data File to load
    @property
    def data_file(self):
        return super().data_file.lower()

    # Type of the data file (CSV | JSON)
    @property
    def file_type(self):
        _file_type = super().file_extension.lower()[1::]
        return _file_type

    ## call_agent_config
    ##
    @property
    def auth_key(self):
        return self._auth_key

    @auth_key.setter
    def auth_key(self, value):
        self._call_agent_config = value

    #
    # Methods
    def load(self):
        data = super().load()
        if self.is_loaded:
            if not self._auth_key == None:
                if not self._data["blandai_auth_key"] == None:
                    self._auth_key = self._data["blandai_auth_key"]
                elif not self._data["auth_key_env"] == None:
                    os = __import__("os")
                    if not os.environ["auth_key_env"] == None:
                        self._auth_key = os.environ["auth_key_env"]
                else:
                    self.auth_key = None
        else:
            self._auth_key = None
        return data

#
# Get settings from app config
