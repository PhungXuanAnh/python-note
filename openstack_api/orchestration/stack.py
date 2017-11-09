import requests
import json
import urlparse
import urllib2
import logging

class Stacks(object):
    
    def __init__(self, os_token, os_heat_url):
        self.os_token = os_token
        self.heat_url = os_heat_url+ '/stacks'
        
    def list(self):    
        headers = {
            'X-Auth-Token': self.os_token,
        }
        
        return requests.get(self.heat_url, headers=headers)
    
    def __delete(self, stack_url):
        headers = {
            'X-Auth-Token': self.os_token,
        }
        
        return requests.delete(stack_url, headers=headers)
        
    def delete(self, stack_name):
        for stack in json.loads(self.list().text)["stacks"]:
            if stack["stack_name"] == stack_name:
                for link in stack["links"]:
                    if link["rel"] == "self":
                        self.__delete(link["href"])
        
if __name__ == '__main__':
#     heat_client = HeatStack()
#     print json.dumps(json.loads(heat_client.list().text), indent=4, sort_keys=True)
    pass