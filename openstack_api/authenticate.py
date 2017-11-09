'''
Created on Dec 30, 2016

@author: xuananh

this is authenticate api v3
'''

import requests
import json

class Authenticate(object):
    
    def __init__(self, OS_AUTH_URL, OS_PROJECT_NAME, OS_USERNAME, OS_PASSWORD, 
                 OS_USER_DOMAIN_NAME='default',
                 OS_PROJECT_DOMAIN_NAME='default'):
        
        self.link_t = OS_AUTH_URL + '/auth/tokens'

        self.headers = {
            'Content-Type': 'application/json',
            }
        
        self.data = { 
            "auth": { 
                "identity": { 
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "domain": {
                                "name": OS_USER_DOMAIN_NAME
                            },
                            "name": OS_USERNAME, 
                            "password": OS_PASSWORD
                        }                                 
                    } 
                }, 
                "scope": { 
                    "project": { 
                        "domain": { 
                            "name": OS_PROJECT_DOMAIN_NAME
                        }, 
                        "name":  OS_PROJECT_NAME 
                    } 
                } 
            }
        }
        
        self.response=requests.post(self.link_t, headers=self.headers, data=json.dumps(self.data))
        '''
        Response status code:
        201: authenticate success
        401: unauthorized error occurs
        404: resource could bot be found 
        '''
        
        self.token_id = None
        self.compute_admin_url = None
        self.image_admin_url = None
        self.network_admin_url = None
        self.orchestration_admin_url = None
        
        if self.response.status_code == 201:
            self.token_id = self.response.headers["X-Subject-Token"]
            
            self.response = json.loads(self.response.text)
            for val in self.response["token"]["catalog"]:
                
                if val["type"] == "image":
                    for val1 in val["endpoints"]:
                        if val1["interface"] == "admin":
                            self.image_admin_url = val1["url"]
                            
                if val["type"] == "network":
                    for val1 in val["endpoints"]:
                        if val1["interface"] == "admin":
                            self.network_admin_url = val1["url"]
                
                if val["type"] == "orchestration":
                    for val1 in val["endpoints"]:
                        if val1["interface"] == "admin":
                            self.orchestration_admin_url = val1["url"]
                
                if val["type"] == "compute":
                    for val1 in val["endpoints"]:
                        if val1["interface"] == "admin":
                            self.compute_admin_url = val1["url"]
                
        else:
            raise ValueError("Openstack authentication failed: ", self.response.text)
            
     
    def get_authenticate_result(self):
        return self.response
                
    def get_token_id(self):
        return self.token_id
    
    def get_compute_admin_url(self):
        return self.compute_admin_url
                
    def get_image_admin_url(self):
        return self.image_admin_url
    
    def get_orchestration_admin_url(self):
        return self.orchestration_admin_url  
    
    def get_network_admin_url(self):
        return self.network_admin_url
    