import json
from openstack_api.client import Client

OS_AUTH_URL='http://10.76.241.99:5000/v3'
OS_PROJECT_NAME='admin'
OS_USERNAME='admin'
OS_PASSWORD='281bb774aa104179'
    
if __name__ == '__main__':
    dict_flavorProperties = {
                "flavor":{
                    "name":"test_flavor194",     
                    "ram": 1024,               
                    "disk": 10,                
                    "vcpus": 2,                 
                    "OS-FLV-EXT-DATA:ephemeral": 1,
                    "swap": 1,  
                    "rxtx_factor": 1.0,
                    "os-flavor-access:is_public": True                                                     
                }
            }
    dict_extraSpecs =         {
            "extra_specs": {
                "hw:cpu_cores": "14",
                "hw:cpu_sockets": "1"
            }
        }
    
    flavorProperties = json.dumps(dict_flavorProperties)
    extraSpecs = json.dumps(dict_extraSpecs)
    
    json_image_properties = {
            "container_format": "bare", 
            "disk_format": "qcow2", 
            "name": "demo20"
        }
    'Down load image'
#     url = 'https://uec-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img'
#     split = urlparse.urlsplit(url)
#     filename = "/tmp/" + split.path.split("/")[-1]
#     
#     try:        
#         print ("downloading with urllib2")
#         f = urllib2.urlopen(url)
#         data = f.read()
#         with open(filename, "wb") as code:
#             code.write(data)
#         print ("download complete")
#     except:
#         logging.exception("Downloading error 2: ") 
#     
#     response = image.create_image(image_properties = json.dumps(json_image_properties), 
#                         path_to_image = filename)
#     response = image.create_image_primary(image_properties = json.dumps(json_image_properties))
#     response = client.flavor.create(flavorProperties, extraSpecs)
    
    client = Client(OS_AUTH_URL=OS_AUTH_URL, 
                    OS_PROJECT_NAME=OS_PROJECT_NAME,
                    OS_USERNAME=OS_USERNAME, 
                    OS_PASSWORD=OS_PASSWORD)
#     response = client.image.list()    

#     response = client.heat.stacks.list()
    response = client.heat.stacks.delete(stack_name = "demo-59c93184")
    try:
        parsed = json.loads(response.text)
        print json.dumps(parsed, indent=4, sort_keys=True)
    except:
        print ("status code: ", response.status_code)
        print response.text
        

