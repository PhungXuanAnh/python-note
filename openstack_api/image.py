'''
Created on Dec 30, 2016

@author: xuananh
'''
import requests
import json
import urlparse
import urllib2
import logging

class Image(object):
    
    def __init__(self, os_token, os_image_url):
        self.os_token = os_token
        self.os_image_url = os_image_url
        self.image_url = str(self.os_image_url) + '/v2/images'    
        
    '''    
    @list:
    '''
    def list(self):    
        headers = {
            'X-Auth-Token': self.os_token,
        }
        
        return requests.get(self.image_url, headers=headers) 
    
    '''    
    @__create:
        json_image_properties = {
            "container_format": "bare", 
            "disk_format": "qcow2", 
            "name": "demo20"
        }
    Return:
        Normal response codes: 201
        Error response codes: 400, 401, 403, 409, 413, 415
    '''
    def __create(self, image_properties):
        headers = {
            'X-Auth-Token': self.os_token,
        }
#         data = '{"container_format": "bare", "disk_format": "qcow2", "name": "demo20"}'
        return requests.post(self.image_url, headers=headers, data=image_properties)       

    '''    
    @__upload:
    Return:
        Normal response codes: 204
        Error response codes: 400, 401, 403, 404, 409, 410, 413, 415, 503
    '''
    def __upload(self, path_to_image, file_image_link):
        print("__uploading image...")
        headers = {
            'X-Auth-Token': self.os_token,
            'Content-Type': 'application/octet-stream',
        }
         
        data = open(path_to_image, 'rb').read()
        return requests.put(file_image_link, headers=headers, data=data)

    '''    
    @create:
    ''' 
    def create(self, image_properties, imageLocation = None, imageUrl = None):
        response = self.__create(image_properties)
        if (response.status_code != 201): return response
        
        dict_response = json.loads(response.text)
        file_image_link = self.os_image_url + dict_response["file"]
        
        if imageLocation != None :
            return self.__upload(imageLocation, file_image_link)
        
        if imageUrl != None :
            split = urlparse.urlsplit(imageUrl)
            filename = "/tmp/" + split.path.split("/")[-1]
            try:        
                print ("downloading image...")
                f = urllib2.urlopen(imageUrl)
                data = f.read()
                with open(filename, "wb") as code:
                    code.write(data)
                print ("download complete.")
            except:
                self.delete(dict_response["id"])
                logging.exception("Download image error: ")
            
            return self.__upload(filename, file_image_link)

        self.delete(dict_response["id"])
        raise ValueError("Neither imageLocation or imageUrl is not provided")      
        
    '''    
    @delete:
    '''    
    def delete(self, imageId):
        headers = {
            'X-Auth-Token': self.os_token,
        }

        return requests.get(self.os_image_url + '/v2/images/' + imageId, headers=headers)
