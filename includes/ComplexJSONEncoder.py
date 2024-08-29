import json
import inspect

class ComplexJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, dict):
                return {key: self.default(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [self.default(item) for item in obj]
            else:
                return obj
        except Exception as e:
            print(e)
            return None
        
class ComplexJSON(object):
    def __init__(self, json_dict):
        for key, value in json_dict.items():
            setattr(self, key, value)
    #def __repr__(self):
    #    return self._str_val
    def show(self):
        for i in inspect.getmembers(self):
            
            # to remove private and protected
            # functions
            if not i[0].startswith('_'):
                
                # To remove other methods that
                # doesnot start with a underscore
                if not inspect.ismethod(i[1]): 
                    print(i)

class JSONToClass: 
    def __init__(self, json_object):
        self._json_object = json_object
    def convert(self):
        try:
            json_string = json.dumps(self._json_object, cls=ComplexJSONEncoder, indent=2)
            # print("internal===>",json_string)
            return json.loads(json_string, object_hook=lambda d: ComplexJSON(d))
        except Exception as e:
            print(e)
            return None



# Example usage:
"""
json_object = {
    "name": "John Doe",
    "age": 30,
    "occupation": "Software Engineer",
    "hobbies": ["coding", "reading", "traveling"]
}

complex_json_object = convert_json_to_class(json_object)

print(complex_json_object.name)  # "John Doe"
print(complex_json_object.age)  # 30
print(complex_json_object.occupation)  # "Software Engineer"
print(complex_json_object.hobbies)  # ["coding", "reading", "traveling"]
"""