import argparse
import sys
import os
import json
import pandas as pd
#import numpy as np
import requests
import schedule
import time

from includes.AppConfig import AppConfig
from includes.CallAgent import CallAgent
from includes.ComplexJSONEncoder import JSONToClass   

###########################
# Arguments for the agent
###########################
if __name__ == '__main__':

    def run_batch_caller():

        ###########################
        # Initilize the application
        ###########################

        # Open the App Config JSON file
        #
        my_obj = AppConfig('./config/app_config.json')
        app_config_json = my_obj.load()

        # Json to Class
        my_class = JSONToClass(app_config_json)
        app_config = my_class.convert()

        if __debug__:
            print()
            print("Loaded App config")
            print()
            app_config.show()


        ###########################
        # Initialize the CallAgent
        ###########################

        blandai_auth_key = os.environ[app_config.auth_key_env] 
        call_agent = CallAgent(blandai_auth_key) 
        #call_agent.test_mode = args.testmode 

        print()
        print("Sending Call Batch")
        call_info = call_agent.send_call_batch(args.call_file)

        print()
        print("Batch Send Info")
        print(call_info)
        exit(1)

###########################
# Call every
###########################
schedule.every(5).minutes.do(run_batch_caller) 
  
while True: 
    schedule.run_pending() 
    time.sleep(1) 