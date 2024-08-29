# from sys import path
# path.append('./includes')
from includes.AppConfig import AppConfig
from includes.CallConfig import CallConfig
from includes.CallData import CallData 
from includes.ComplexJSONEncoder import JSONToClass
import json

#########################
# Test AppConfig Class
#########################
my_class = AppConfig('./config/app_config.json')
file_content = my_class.load()

json_obj = JSONToClass(file_content)
complex_json_object = json_obj.convert()

print()
print("AppConfig Class")
print(my_class.data_file)
print(my_class.file_type)
print(file_content)
print(type(file_content))
print(type(complex_json_object))
complex_json_object.show()
print( complex_json_object.api_batch_call_url)

#########################
# Test CallConfig Class
#########################
my_class = CallConfig('./config/call_config.json')
file_content = my_class.load()

json_obj = JSONToClass(file_content)
complex_json_object = json_obj.convert()

print()
print("CallConfig Class")
print(my_class.data_file)
print(my_class.file_type)
print(file_content)
print(type(file_content))
print(type(complex_json_object))
complex_json_object.show()

#########################
# Test CallData Class
#########################
my_class = CallData("./data/call_list_test.csv")
file_content = my_class.load()

print()
print("CallData Class")
print(my_class.data_file)
print(my_class.file_type)
print(file_content)
print(type(file_content))

#########################
# Test ComplexJSONEncoder
#########################
print()
print("ComplexJSONEncoder Class")

json_obj = JSONToClass(json.loads(file_content))
complex_json_object = json_obj.convert()
print()
print(type(complex_json_object))
print(complex_json_object[0].office)
complex_json_object[0].show()

json_string = """
{
    "name": "John Doe",
    "age": 30,
    "occupation": "Software Engineer"
}
"""
print()
print("ComplexJSONEncoder Class")

json_obj = JSONToClass(json.loads(json_string))
complex_json_object = json_obj.convert()
print()
print(type(complex_json_object))
complex_json_object.show()


