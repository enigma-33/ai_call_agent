import sys
import os
import json
import pandas as pd
#import numpy as np
import requests

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from datetime import datetime
from includes.AppConfig import AppConfig
from includes.CallAgent import CallAgent
from includes.ComplexJSONEncoder import JSONToClass   


description = """
#TranquityX AI Caller Agent API
Enables you to configure, schedule, and send automated, interactive calls to lists of receivers . 🚀

## Items
You can .

## Users
You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="TranquilityX AI | Caller Agent API",
    description=description,
    summary="TranquilityX AI's AI Caller Agent API.",
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "TranquityX AI Contact Info",
        "url": "https://www.tranquilityx.ai/contact",
        "email": "info@tranquilityx.ai",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


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

###########################
# Initialize Agent
###########################

blandai_auth_key = os.environ[app_config.auth_key_env] 
call_agent = CallAgent(blandai_auth_key) 


@app.get("/")
def read_root():
    return {"TranquilityX AI": "AI Caller Agent initialized"}

###########################
# Config endpoints
###########################

## TODO: 
## Need:
## 1. Get/Set Company Name
## 2. Get/Set Multiple Config Files
## 3. Get/Set API Key

@app.get("/v1/config/app")
def get_app_config():
    return {"TxAI | App Config" : app_config}

@app.get("/v1/config/call/single")
def get_single_call_config():
    return {"TxAI | Single Call Config" : call_agent.single_call_config}

@app.get("/v1/config/call/batch")
def get_batch_call_config():
    return {"TxAI | Batch Call Config" : call_agent.batch_call_config}

###########################
# Call endpoints
###########################
