'''
Created on Mar 1, 2017

@author: xuananh

this modules use to save an python object
'''

import pickle

class Company(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

with open('pickle_company_data.pkl', 'wb') as output_data:
    
    company2 = Company('bbbbbbbbb', 42)
    pickle.dump(company2, output_data, pickle.HIGHEST_PROTOCOL)
    
    company1 = Company('aaaaaaaaaa', 41)
    pickle.dump(company1, output_data, pickle.HIGHEST_PROTOCOL)



del company1
del company2
