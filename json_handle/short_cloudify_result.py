#!/usr/bin/python

# This only uses the json package
import json

file_path = "/media/xuananh/data/Temp/202-nodes.json"

# Load the contents from the file, which creates a new dictionary 
dict_data = None
list_nodes = None
new_list_nodes = []

with open(file_path,"r") as in_file:
    dict_data = json.load(in_file)
    print (json.dumps(dict_data, indent=4, sort_keys=True))

    list_nodes = dict_data.get("items", None)
    
    for val_node in list_nodes:
        
        if ("cloudify.nodes.Compute" in val_node["type_hierarchy"]) :
            val_node.pop("relationships")
            val_node.pop("plugins")
            val_node.pop("plugins_to_install")
            val_node.pop("operations")
            
            
            if val_node["properties"].get("use_password") != False:
                print (json.dumps(val_node, indent=4, sort_keys=True))
                new_list_nodes.append(val_node)
            
file_path1 = "/media/xuananh/data/Temp/202-nodes.new.json"        
with open(file_path1,"w") as out_file:
    json.dump(new_list_nodes, out_file, indent=4)  
