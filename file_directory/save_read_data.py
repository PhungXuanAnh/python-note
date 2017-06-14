import json
import os

data ={
    "Id": "this is ID",
    "Command": "upload_deployment",
    "Params": [
                  {"name": "image", "value": "123"},
                  {"name": "flavor", "value": "456"},
                  {"name": "agent_user", "value": "centos"}
    ],
    "From": "dashboard"
}

# save data to file #
with open("Output.txt", "w") as text_file:
    text_file.write("This is your string:\n{}".format(json.dumps(data, indent=4)))

# read data from file #
file1 = open('Output.txt', 'r')    
print file1.read()

# As you can see above, there are 2 ways to open a file to handle data #




os.remove("Output.txt")

