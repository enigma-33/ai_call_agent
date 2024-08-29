from includes.CallConfig import CallConfig
from includes.CallData import CallData
from includes.ComplexJSONEncoder import JSONToClass
import requests 

import builtins
import json

class CallAgent:
    _CALL_AGENT_CONFIG_FILE ="./config/call_agent_config.json"
    _SINGLE_CALL_CONFIG_FILE ="./config/single_call_config.json"
    _BATCH_CALL_CONFIG_FILE ="./config/batch_call_config_v1.json"
    _BATCH_CALL_CONFIG_FILE_V2 ="./config/batch_call_config_v2.json"

    def __init__(self, authkey): #, call_list_file):
        self._is_initialized = False
        self._authorization = authkey
        self._config_file = self._CALL_AGENT_CONFIG_FILE
        self._single_call_config_file = self._SINGLE_CALL_CONFIG_FILE
        self._batch_call_config_file = self._BATCH_CALL_CONFIG_FILE
        self._batch_call_config_file_v2 = self._BATCH_CALL_CONFIG_FILE_V2
        self._call_list_file = None 
        self._header = None
        self._endpoints = None
        self._test_mode = False
        self._call_data = None
        self._call_agent_config = None
        self._single_call_config = None
        self._batch_call_config = None
        self._batch_call_config_v2 = None

        if __debug__:
            print()
            print("ready to call CallAgent initialize")
        
        self._initialize()

    ###############################
    # Methods
    ###############################
    def _initialize(self):
        try:
            # ::::::::::::::::::::::::::::::
            # Open the Call Config JSON file
            # ::::::::::::::::::::::::::::::
            my_obj = CallConfig(self.config_file)
            call_agent_config_json = my_obj.load()
            self._call_agent_config = call_agent_config_json

            # :::::::::::::::::::::::::::::::::::::
            # Open the Single Call Config JSON file
            # :::::::::::::::::::::::::::::::::::::
            my_obj = CallConfig(self.single_call_config_file)
            single_call_config_json = my_obj.load()
            self.single_call_config = single_call_config_json

            # :::::::::::::::::::::::::::::::::::::
            # Open the Batch Call Config JSON file
            # :::::::::::::::::::::::::::::::::::::
            my_obj = CallConfig(self.batch_call_config_file)
            batch_call_config_json = my_obj.load()
            self.batch_call_config = batch_call_config_json

            # ::::::::::::::::::::::::::    :::::::::::::
            # Open the Batch Call Config V2 JSON file
            # :::::::::::::::::::::::::::::::::::::::
            my_obj = CallConfig(self.batch_call_config_file_v2)
            batch_call_config_json_v2 = my_obj.load()
            self.batch_call_config_v2 = batch_call_config_json_v2

            # ::::::::::::::::::::::::::::::
            # Set http request header
            # ::::::::::::::::::::::::::::::
            self._set_header()

            self.is_initialized = True
        except Exception as e:
            print(e)
            self.is_initialized = False
            self._call_data = None
        return self.is_initialized
    def _call_endpoint(self, url, payload, headers):
        if __debug__:
            http = __import__(http)
            logging = __import__(logging)
            http.client.HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
        response = requests.post(url, json=payload, headers=headers)

        return response
    def _set_header(self):
        headers = {
            "Authorization": self._authorization,
            "Content-Type": "application/json"
        }
        self._header = headers

        if __debug__:
            print(self._header)

        return
    def send_call(self):
        json_formatted_str = None
        try:
            url = "https://api.bland.ai/v1/calls"
            payload=self.single_call_config
            response = requests.post(url, json=payload, headers=self.header)
            json_obj = json.loads(response.text)
            json_formatted_str = json.dumps(json_obj,indent=2)
        except Exception as e:
            print(e)

        return json_formatted_str
    def stop_call(self):
        return None
    def call_details(self,call_id):
        try:
            url = "https://api.bland.ai/v1/calls/{0}".format(call_id)
            response = requests.get(url, headers=self.header)
            json_obj = json.loads(response.text)
            json_formatted_str = json.dumps(json_obj,indent=2)
        except Exception as e:
            print(e)

        return json_formatted_str
    def send_call_batch(self,call_list_file):
        json_formatted_str = None
        try:
            ## Load the call file. The self.batch_call_config will be reloaded.
            call_data = self.load(call_list_file)
            payload = self.batch_call_config

            ## Send the request
            url = "https://api.bland.ai/v1/batches"
            response = requests.post(url, json=payload, headers=self.header)
            print(response.text)
            json_obj = json.loads(response.text)
            json_formatted_str = json.dumps(json_obj,indent=2)
        except Exception as e:
            print(e)

        return json_formatted_str
    def send_call_batch_v2(self,call_list_file):
        json_formatted_str = None
        try:
            ## Load the call file. The self.batch_call_config will be reloaded.
            call_data = self.load_v2(call_list_file)
            payload = self.batch_call_config_v2
            print(json.dumps(payload,indent=2))

            ## Send the request
            url = "https://api.bland.ai/v2/batches"
            response = requests.post(url, json=payload, headers=self.header)
            print(response.text)
            json_obj = json.loads(response.text)
            json_formatted_str = json.dumps(json_obj,indent=2)
        except Exception as e:
            print(e)

        return json_formatted_str
    def stop_batch(self,batch_id):
        return None
    def batch_details(self,batch_id):
        url = "https://api.bland.ai/v1/batches/{0}".format(batch_id)
        response = requests.get(url, headers=self.header)
        json_obj = json.loads(response.text)
        json_formatted_str = json.dumps(json_obj,indent=2)

        return json_formatted_str
    def list_calls(self):
        url = "https://api.bland.ai/v1/calls"
        response = requests.get(url, headers=self.header)
        json_obj = json.loads(response.text)
        json_formatted_str = json.dumps(json_obj,indent=2)

        return json_obj # json_formatted_str
    def list_batches(self):
        url = "https://api.bland.ai/v1/batches"
        response = requests.get(url, headers=self.header)
        json_obj = json.loads(response.text)
        json_formatted_str = json.dumps(json_obj,indent=2)

        return json_obj
    def analyze_call_ai(self,call_id):
        return None
    def analyze_batch_ai(bself,atch_id):
        return None
    def help():
        return "Usage:"
    def report():
        return None
    def load(self,call_list_file=None):
        # ::::::::::::::::::::::::::::::
        # Read the call data file
        # ::::::::::::::::::::::::::::::
        try:
            if not call_list_file == None:
                my_obj = CallData(call_list_file)
                self.call_data = my_obj.load()

                # reset the payload
                self.batch_call_config = self.batch_call_config
                return self.call_data
            else:
                print("You must provide a valid call list file.")
                return None
        except Exception as e:
            print(e)
    def load_v2(self,call_list_file=None):
        # ::::::::::::::::::::::::::::::
        # Read the call data file
        # ::::::::::::::::::::::::::::::
        try:
            if not call_list_file == None:
                my_obj = CallData(call_list_file)
                self.call_data = my_obj.load()

                # reset the payload
                self.batch_call_config_v2 = self.batch_call_config_v2
                return self.call_data
            else:
                print("You must provide a valid call list file.")
                return None
        except Exception as e:
            print(e)

    ###############################
    # Properties
    ###############################
    
    ## _is_initialized (private)
    ##
    @property
    def is_initialized(self):
        return self._is_initialized

    @is_initialized.setter
    def is_initialized(self, value):
        self._is_initialized = value

    ## test_mode
    ##
    @property
    def test_mode(self):
        return self._test_mode

    @test_mode.setter
    def test_mode(self, value):
        self._test_mode = value

    ## config_file
    ##
    @property
    def config_file(self):
        return self._config_file

    @config_file.setter
    def config_file(self, value):
        # Json to Class
        my_class = JSONToClass(value)
        self._call_agent_config = my_class.convert()

    ## single_call_config_file
    ##
    @property
    def single_call_config_file(self):
        return self._single_call_config_file

    @single_call_config_file.setter
    def single_call_config_file(self, value):
        # Json to Class
        my_class = JSONToClass(value)
        self._single_call_config = my_class.convert()

    ## batch_call_config_file
    ##
    @property
    def batch_call_config_file(self):
        return self._batch_call_config_file

    @batch_call_config_file.setter
    def batch_call_config_file(self, value):
        # Json to Class
        my_class = JSONToClass(value)
        self._batch_call_config = my_class.convert()

    ## batch_call_config_file_v2
    ##
    @property
    def batch_call_config_file_v2(self):
        return self._batch_call_config_file_v2

    @batch_call_config_file_v2.setter
    def batch_call_config_file_v2(self, value):
        # Json to Class
        my_class = JSONToClass(value)
        self._batch_call_config_v2 = my_class.convert()

    ## call_agent_config
    ##
    @property
    def call_agent_config(self):
        return self._call_agent_config

    @call_agent_config.setter
    def call_agent_config(self, value):
        self._call_agent_config = value

    ## single_call__config
    ##
    @property
    def single_call_config(self):
        return self._single_call_config

    @single_call_config.setter
    def single_call_config(self, value):
        data = value
        task_array = data["task"]
        json_object = json.dumps(task_array)

        task = " ".join(json.loads(json_object))
        data["task"] = task
        
        new_data = json.loads(json.dumps(data))
        self._single_call_config = new_data

    ## batch_call__config
    ##
    @property
    def batch_call_config(self):
        return self._batch_call_config

    @batch_call_config.setter
    def batch_call_config(self, value):
        data = value
        base_prompt_array = data["base_prompt"]
        json_object = json.dumps(base_prompt_array,indent=2)

        if self._batch_call_config == None:
            base_prompt = " ".join(json.loads(json_object))
            data["base_prompt"] = base_prompt
            data = json.loads(json.dumps(data))

        if not self.call_data == None:
            call_data_array = self.call_data
            json_object = json.dumps(call_data_array,indent=2)
            data["call_data"] = json.loads(json_object)
            data = json.loads(json.dumps(data))
        
        self._batch_call_config = data

    ## batch_call__config_v2
    ##
    @property
    def batch_call_config_v2(self):
        return self._batch_call_config_v2

    @batch_call_config_v2.setter
    def batch_call_config_v2(self, value):
        data = value

        base_prompt_array = data["call_params"]["task"]
        json_object = json.dumps(base_prompt_array,indent=2)

        if self._batch_call_config_v2 == None:
            base_prompt = " ".join(json.loads(json_object))
            data["call_params"]["task"] = base_prompt
            data = json.loads(json.dumps(data))

        if not self.call_data == None:
            call_data_array = self.call_data
            json_object = json.dumps(call_data_array,indent=2)
            data["call_data"] = json.loads(json_object)
            data = json.loads(json.dumps(data))
        
        self._batch_call_config_v2 = data

    ## call_list_file
    ##
    @property
    def call_list_file(self):
        return self._call_list_file

    @call_list_file.setter
    def call_list_file(self, value):
        self._call_list_file = value

    ## data
    ##
    @property
    def call_data(self):
        return self._call_data

    @call_data.setter
    def call_data(self, value):
        self._call_data = value

    ## header
    ##
    @property
    def header(self):
        return self._header
    
    ## debug
    ##
    @property
    def debug(self):
        return __debug__
    
