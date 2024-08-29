import argparse
import sys
import os
import json
import pandas as pd
#import numpy as np
import requests

from datetime import datetime
from includes.AppConfig import AppConfig
from includes.CallAgent import CallAgent
from includes.ComplexJSONEncoder import JSONToClass   

###########################
# Arguments for the agent
###########################
if __name__ == '__main__':
    command_parser = argparse.ArgumentParser(description="Argument parser",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = command_parser.add_subparsers(dest='command')

    send_call  = subparsers.add_parser('send_call', help='Place a single call')
    send_call_batch  = subparsers.add_parser('send_call_batch', help='Process a batch call file')
    send_call_batch.add_argument("--call_file", required=True ,default=None, help="Call List File.  csv | json") 
    send_call_batch.add_argument("--testmode", required=False ,default=0, help="Set test mode True | False.") 
    send_call_batch_v2  = subparsers.add_parser('send_call_batch_v2', help='Process a batch call file (v2)')
    send_call_batch_v2.add_argument("--call_file", required=True ,default=None, help="Call List File.  csv | json") 
    send_call_batch_v2.add_argument("--testmode", required=False ,default=0, help="Set test mode True | False.") 
    list_calls = subparsers.add_parser('list_calls', help='List calls made for your account')
    list_batch  = subparsers.add_parser('list_batches', help='List batch calls made for your account')
    call_details  = subparsers.add_parser('call_details', help='Get the call details for the specified call id')
    call_details.add_argument('--id', required=True, action='store', dest="id", help='Call ID')
    batch_details  = subparsers.add_parser('batch_details', help='Get the batch details for the specified batch id')
    batch_details.add_argument('--id', required=True, action='store', dest="id", help='Call ID')
    update_batch_results  = subparsers.add_parser('update_batch_results', help='Get the batch details for the specified batch id')
    update_batch_results.add_argument('--id', required=True, action='store', dest="id", help='Call ID')
    update_batch_results.add_argument("--call_file", required=True ,default=None, help="Call List File.  csv | json") 

    args = command_parser.parse_args()
    config = vars(args)

    if __debug__:
        print()
        print("Runtime parameters")
        print(config)

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

# Get start time
start_datetime = datetime.now()
start_datetime_str = start_datetime.strftime('%Y%m%d_%H%M%S')

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

###########################
# Run the command requested
###########################
if args.command == "list_calls":
    print()
    print("Listing Calls")
    call_info = call_agent.list_calls()
    count = call_info["count"]
    calls = call_info["calls"]

    print()
    print("Count: ", count)
    print("Calls: ")
    print("\tID: {:<45s}DATE {:<40s}COMPLETED".format("",""))
    cx = 1
    for i in calls:
        print("{:3}\t{:40}{:<9s}{:<35s}{:<10s}{:<5b}".format(cx,i["c_id"],"",i["created_at"],"",i["completed"]))  
        cx += 1      
    exit(1)
elif args.command == "list_batches":
    print()
    print("Listing Batches")
    batch_info = call_agent.list_batches()
    count = len(batch_info)
    batches = batch_info["batches"]

    print()
    print("Count: ", count)
    print("Batches: ")
    print("\tID: {:<45s}DATE".format(""))
    cx = 1
    for i in batches:
        print("{:<3}\t{:40}{:<9s}{:<35s}".format(cx,i["batch_id"],"",i["created_at"]))  
        #print("{:3i}\t{:40}{:<9s}{:<35s}".format(cx,i["batch_id"],"",i["created_at"]))  
        cx += 1      
    exit(1)
elif args.command == "call_details":
    print()
    print("Listing Call Details")
    call_info = call_agent.call_details(args.id)

    print("id", args.id)
    print(call_info)
    exit(1)
elif args.command == "batch_details":
    print()
    print("Listing Batch Details")
    batch_info = call_agent.batch_details(args.id)
    json_data = json.loads(batch_info)

    #print(json_data["analysis"])
    #print(type(json_data))
    excel_filename = './output/json_data_to_excel.xlsx'

    # Dump Pandas DataFrame to Excel sheet
    df = pd.DataFrame()

    ######## Analysis Data
    analysis_data = json_data["analysis"] 
    analysis_df = pd.json_normalize(analysis_data)
    print(analysis_df)

    analysis_df = analysis_df.transpose()
    print(analysis_df)
    
    # append the new row to the DataFrame
    #df = df._append(analysis_df, ignore_index=True)
    # Concatenate the dataframes vertically
    df = pd.concat([df, analysis_df], axis=0)

    print(df)

    # Instantiate the Excel Writer
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Analysis', index=True, startrow=2)

    # Get book and sheet objects for futher manipulation below
    book = writer.book
    sheet = writer.sheets['Analysis']

    # Title
    bold = book.add_format({'bold': True, 'size': 24})
    sheet.write('A1', 'Analysis', bold)

    ######### Call Data
    call_data = json_data["call_data"]
    call_df = pd.DataFrame(call_data)
    print(call_data)

    call_df.to_excel(writer,sheet_name="Calls", index=False, startrow=2)

    # Title
    sheet = writer.sheets['Calls']
    bold = book.add_format({'bold': True, 'size': 24})
    sheet.write('A1', 'Calls', bold)

    ######## Batch Param Data
    param_data = json_data["batch_params"]
    #param_df = pd.DataFrame(param_data)
    param_df = pd.json_normalize(param_data)
    param_df = param_df.transpose()
    print(param_data)

    param_df.to_excel(writer,sheet_name="BatchParams", index=True, startrow=2)

    # Title
    sheet = writer.sheets['BatchParams']
    bold = book.add_format({'bold': True, 'size': 24})
    sheet.write('A1', 'Batch Params', bold)
    writer.close()

    print("")
    print("id", args.id)
    #print(batch_info)
    exit(1)
elif args.command == "send_call":
    print()
    print("Sending Single Call")
    call_info = call_agent.send_call()
    print(call_info)
    exit(1)
elif args.command == "send_call_batch":
    print()
    print("Sending Call Batch")
    call_info = call_agent.send_call_batch(args.call_file)

    print()
    print("Batch Send Info")
    print(call_info)
    exit(1)
elif args.command == "send_call_batch_v2":
    print()
    print("Sending Call Batch v2")
    call_info = call_agent.send_call_batch_v2(args.call_file)

    print()
    print("Batch Send Info")
    print(call_info)
    exit(1)
elif args.command == "update_batch_results":
    ## TODO: Add Excel as accepted format and modify DataFile.py load()
    ## TODO: Update original call file with the 
    print()
    print("Updating Batch Call File with Results")
    batch_info = call_agent.batch_details(args.id)
    json_data = json.loads(batch_info)

    #print(json_data)

    if json_data["status"] == "completed":
        print("...Batch has completed.")
        
        base_path = os.path.dirname(args.call_file)
        file_name = os.path.basename(args.call_file)
        name, extension = os.path.splitext(file_name)
        seperator = "_"
        result_call_file = os.path.join(base_path, seperator.join([start_datetime_str,name,"results"]) + extension)
        print("...Results will be written to ",result_call_file)

        #df = pd.read_csv(args.call_file)
        call_data = json_data["call_data"]
        #print(type(call_data))
        #print(call_data)

        df_results = pd.DataFrame()
        for dict in call_data:

            #print(dict["to"])
            #print(dict["variables"]["last_name"])

            result_dict = {}
            result_dict["call_placed_at"] = dict["created_at"]
            result_dict["last_name"] = dict["variables"]["last_name"]
            result_dict["first_name"] = dict["variables"]["first_name"]
            result_dict["to"] = dict["to"]
            result_dict["from"] = dict["from"]
            result_dict["original_appt_time"] = dict["variables"]["appt_time"]
            result_dict["status"] = dict["status"]
            result_dict["answered_by"] = dict["answered_by"]
            result_dict["transferred_to"] = dict["transferred_to"]

            #new_df = pd.DataFrame(result_dict)
            #df_results = pd.concat(df_results, new_df)
            #df_results = df_results.append(result_dict, ignore_index=True)
            df_results = pd.concat([df_results, pd.DataFrame([result_dict])], ignore_index=True)
            #df_results.iloc[-1] = result_dict
            #print(result_dict)

        print("Updated status")
        print(df_results)
        df_results.to_csv(result_call_file, index=False)

        #print("type 2", type(json_data))
        #print(json_data)
    else:
        print("...Still Executing Batch")

else:   
    print()
    print("nada")
    exit(0)


