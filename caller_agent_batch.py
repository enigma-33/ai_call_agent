import argparse
import sys
import os
import json
import pandas as pd
import requests

from includes.AppConfig import AppConfig
from includes.ComplexJSONEncoder import JSONToClass   


###########################
# Arguments for the agent
###########################
parser = argparse.ArgumentParser(description="Argument parser",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--file", type=argparse.FileType('r'), default=sys.stdin, help="call list file to process")
parser.add_argument("-r", "--rownum", default=1,help="row of call list to use when mode = single")
parser.add_argument("mode", choices=['single','batch'], default='single', help="run in single call or batch call mode") 
args = parser.parse_args()
config = vars(args)

###########################
# Initilize the application
###########################

# Get the configuration files
#

#
# Open the app config JSON file
app_config = JSONToClass('./config/app_config.json')

print()
print(app_config)

#
# Get settings from app config
auth_key_env = app_config['auth_key_env']
phone_number_env = app_config['phone_number_env']
api_batch_call_url = app_config['api_batch_call_url']

#
# Open the call JSON file
with open('./config/call_config.json', 'r') as f:
    call_config = json.load(f)
f.close()

#
# Get task which is multiline string array in json
task_array = call_config['task']
json_object = json.dumps(task_array)
task = " ".join(json.loads(json_object))

#
# Get example (few-shot) which is multiline string array in json
example_array = call_config['example']
json_object = json.dumps(example_array)
example = " ".join(json.loads(json_object))

#
# Complete Task = task + example
complete_task = task + " " + example

print()
print("Task: ",complete_task)
print()
print(call_config['request_data'])

#
# Get environment variable values
blandai_auth_key = os.environ[auth_key_env] 
blandai_phone_number = os.environ[phone_number_env]

###########################
# Read the office data file
###########################

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('./data/office_list-1.csv')

# Print the column names
print()
print(df.columns)

# Extract the values from the 'Name' column
office_names = df['office_name']

# Print the values
print()
print(office_names)

# Convert the DataFrame to a JSON object
json_office_data = df.to_json(orient='records')

# Print the JSON object
print()
print(json_office_data)

###########################
# Read the call data file
###########################

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('./data/call_list-1.csv')

# Print the column names
print()
print(df.columns)

# Extract the values from the 'Name' column
names = df['last_name']

# Print the values
print()
print(names)

# Convert the DataFrame to a JSON object
json_call_data = df.to_json(orient='records')

# Print the JSON object
print()
print(json_call_data)

###########################
# Make the phone call)s)
###########################

# Headers
headers = {
    "Authorization": blandai_auth_key,
    "Content-Type": "application/json"
}
json_headers = json.dumps(headers)

print()
print(headers)
print()
print(blandai_phone_number)

base_prompt = complete_task 
#"You are calling {{business}} to renew their subscription to {{service}} before it expires on {{date}}."
call_data = [
    {
        "office": "office-1",
        "last_name": "Leisman",
        "first_name": "Ed",
        "phone_number": 17244130489,
        "language": "eng"
    },
    {
        "office": "office-1",
        "last_name": "Lemus",
        "first_name": "Jose",
        "phone_number": 17244130489,
        "language": "esp"
    },
    {
        "office": "office-2",
        "last_name": "Mouse",
        "first_name": "Minnie",
        "phone_number": 17244130489,
        "language": "eng"
    }
]
payload = {
    "base_prompt": base_prompt,
    "call_data": call_data,
    "label": "batch_test_p1",
    "campaign_id": "3333-1",
    "test_mode": True,
    "voice_id": call_config["voice_id"],
    "reduce_latency": call_config["reduce_latency"],
    "request_data": call_config["request_data"],
    "voice_settings": call_config["voice_settings"],
    "interruption_threshold": call_config["interruption_threshold"],
    "start_time": call_config["start_time"],
    "transfer_phone_number": call_config["transfer_phone_number"],
    "answered_by_enabled": call_config["answered_by_enabled"],
    "from": call_config["from"],
    "first_sentence": call_config["first_sentence"],
    "record": call_config["record"],
    "max_duration": call_config["max_duration"],
    "model": call_config["model"],
    "language": call_config["language"]
}


print()
print("Payload:", payload)
print(type(payload))

# Convert Python to JSON  
json_data = json.dumps(payload, indent = 4) 
print()
print("************************")
print(type(json_data))
print(json_data) 

# API request 
print()
print(api_batch_call_url)
print()
print(json_data)
print()
print(json_headers)
print()
print(type(json.dumps(headers)))

import http
import logging
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

response = requests.post(api_batch_call_url, json=payload, headers=headers)
print()
print(response.status_code)             
print(response.text)