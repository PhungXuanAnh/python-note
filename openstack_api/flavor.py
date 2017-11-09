'''
Created on Dec 30, 2016

@author: xuananh
'''
import requests
import json

class Flavor(object):
    
    def __init__(self, os_token, os_compute_url):
        self.os_token = os_token
        self.os_compute_url = os_compute_url
        self.flavor_url = str(self.os_compute_url) + '/flavors'
    
    '''
    @list: __lists all flavors accessible to your project.
    Normal response codes: 200
    Error response codes: unauthorized(401), forbidden(403)
    '''
    def list(self):    
        headers = {
            'X-Auth-Token': self.os_token,
        }
        
        return requests.get(self.flavor_url, headers=headers)
    
    '''
    @__create flavor with properties as below
            {
                "flavor":{
                    "name":"test_flavor1",                 string
                    "id": "11",                            string
                    "ram": 1024,                           integer
                    "disk": 10,                            integer
                    "vcpus": 2,                            integer 
                    "OS-FLV-EXT-DATA:ephemeral": 0,        integer (default)
                    "swap": 0,                             integer (default)
                    "rxtx_factor": 1.0,                    float   (default)
                    "os-flavor-access:is_public": True     boolean (default)
                }
            }
    Params:
        @flavor_properties: string properties of flavor
    Return:
        Normal response codes: 200
        Error response codes: badRequest(400), unauthorized(401), 
                                forbidden(403), conflict(409)
    '''
    def __create(self, flavor_properties):
        headers = {
            'X-Auth-Token': self.os_token,
            'Content-type': 'application/json',
        }
        
#         data = '{"flavor":{"name":"test_flavor1","ram": 1024,"vcpus": 2,"disk": 10,"id": "11","rxtx_factor": 2.0}}'
        return requests.post(self.flavor_url, headers=headers, data=flavor_properties)
    
    def create(self, flavorProperties, extraSpecs = None):
        # return 200 is SUCCESS
        createFv = self.__create(flavorProperties)
        if (extraSpecs == None or createFv.status_code != 200): return createFv
        else:
            setExtra = self.__set_extra_specs(json.loads(createFv.text)["flavor"]["id"], extraSpecs)
            '''
            if set extra specs success then return create flavor result
            else delete flavor and return set extra result
            '''
            if (setExtra.status_code == 200): return createFv
            else:
                self.delete(json.loads(createFv.text)["flavor"]["id"])
                return setExtra
            
    '''
    @delete
    '''
    def delete(self, flavor_id):
        headers = {
            'X-Auth-Token': self.os_token,
        }
        return requests.delete(self.flavor_url + '/' + flavor_id, headers=headers)
        
    '''
    @get: Shows details for a flavor.
    Normal response codes: 200
    Error response codes: unauthorized(401), forbidden(403), itemNotFound(404)
    '''
    def get(self, flavor_id):
        pass   
    
    '''
    @set_extra_specs: input is id flavor
        {
            "extra_specs": {
                "key1": "value1",
                "key2": "value2"
            }
        }
    Return:
        Normal response codes: 200
        Error response codes: unauthorized(401), forbidden(403), itemNotFound(404), conflict(409)        
    '''
    def __set_extra_specs(self, flavor_id, extra_specs):
        headers = {
            'X-Auth-Token': self.os_token,
        }
        
        link_extra_specs = self.flavor_url + '/' + flavor_id + '/os-extra_specs'
        return requests.post(link_extra_specs, headers=headers, data=extra_specs)
    
    '''
    @set_extra_specs input is name flavor 
    '''
    def set_extra_specs(self, extra_specs, flavor_name = None, flavor_id = None):
        if(flavor_id != None):
            return self.__set_extra_specs(flavor_id, extra_specs)
        if (flavor_name != None):
            response = self.__list_flavor()
            dict_flavor = json.loads(response.text)
            __list_flavor = dict_flavor["flavor"]
            for val in __list_flavor:
                if (val["name"] == flavor_name):
                    flavor_id = val["id"]
                    return self.__set_extra_specs(flavor_id, extra_specs)
        return { 
                "Status_code": -1,
                "Result": "Either flavor_name or flavor_id are not provided"
            }
        
                