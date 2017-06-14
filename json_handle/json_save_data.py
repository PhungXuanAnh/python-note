#!/usr/bin/python
import json

dict_data= {
        "path":"abc",
        "list_deployment": []
        }

file_path = "test.json"

with open(file_path,"w") as out_file:
    # Save the dictionary into this file
    # (the 'indent=4' is optional, but makes it more readable)
    json.dump(dict_data,out_file, indent=4)                                    
    
