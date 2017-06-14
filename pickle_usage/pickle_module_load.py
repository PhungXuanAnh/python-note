'''
Created on Mar 1, 2017

@author: xuananh

this modules use to save an python object
'''

import pickle

from pickle_usage.pickle_module_save import Company

with open('pickle_company_data.pkl', 'rb') as input_data:
    company = pickle.load(input_data)
    print(company.name)  # -> banana
    print(company.value)  # -> 40

    company2 = pickle.load(input_data)
    print(company2.name) # -> spam
    print(company2.value)  # -> 42
