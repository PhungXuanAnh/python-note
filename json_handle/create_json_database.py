import urllib2
import logging
import zipfile
import os
import json


sample = {
    "blueprint_id1": {
        "path":"abc",
        "list_deployment": []
        },
    "blueprint_id2": {
        "path":"abc2",
        "list_deployment": []
        }
    }

def download_file(link_archive, path_file):
    try:        
        print("Downloading with urllib2")
        f = urllib2.urlopen(link_archive)
        data = f.read()
        with open(path_file, "wb") as code:
            code.write(data)
        print "aaaaaaaaa 1"
        return '0'
    except:
        logging.exception("Downloading error: ")
        print "aaaaaaaaa 2"        
        return 'error'
        
        
def extract_file(path_to_zip_file, directory_to_extract_to):
    try:
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(directory_to_extract_to)
        list_t = zip_ref.namelist()
        zip_ref.close()
        print "aaaaaaaaa 3"
        return list_t[0]
    except:
        logging.exception("Error while extract file: " + path_to_zip_file)
        print "aaaaaaaaa 4"        
        return 'error'
        
def make_sure_path_exists(path):
    if os.path.exists(path):
        print "aaaaaaaaa 5"         
        return '0'
    else: 
        try:
            os.makedirs(path)
            print "aaaaaaaaa 6"            
            return '0'
        except:
            logging.exception("Error at while create folder: " + path)
            print "aaaaaaaaa 7" 
        return 'error'
        
def change_database(blueprint_id, path_to_blueprint, path_to_json_database):
    # prepair data
    data_t = {
        blueprint_id: {
            "path" : path_to_blueprint, 
            "list_deployment": []
            }
        }
    dict_data = ''
    try:
        # save data
        if (os.path.exists(path_to_json_database)):
            print "aaaaaaaaaaa 8"        
            in_file = open(path_to_json_database, 'r') #open
            dict_data = json.load(in_file)  # read
            dict_data[blueprint_id] = data_t[blueprint_id] # modify
            in_file = open(path_to_json_database, 'w+') #create new
            json.dump(dict_data,in_file, indent=4)   # save
            in_file.close()  
        else:
            print "aaaaaaaaaaa 9"        
            in_file = open(path_to_json_database, 'w') # create and open
            json.dump(data_t,in_file, indent=4)   # save  
            in_file.close()
        return 0
    except:
        logging.exception("Error")
        return -1       
        
def create_database(link_archive, blueprint_id):        
    link_archive = 'https://www.dropbox.com/s/pk5xhnnzay114cr/temp.zip?dl=1'
    path_file = '/media/xuananh/data/Temp/abc.zip'
    path_to_zip_file = path_file
    directory_to_extract_to = '/media/xuananh/data/Temp/test123a/'
#     directory_to_extract_to = '/root/test'
    
    if (download_file(link_archive, path_file) == 'error'): return
    if (make_sure_path_exists(directory_to_extract_to) == 'error'): return
    extract_t = extract_file(path_to_zip_file, directory_to_extract_to)   
    if (extract_t == 'error'): return
    
    blueprint_id = 'abc123a'
    path_to_blueprint = directory_to_extract_to + extract_t
    path_to_json_database = 'database.json'
    
    change_database(blueprint_id, path_to_blueprint, path_to_json_database)

create_database('', '')