'''
Created on Apr 12, 2017

@author: xuananh
'''
import traceback, sys, json

try:
    aaaaaaaaaaaaaaa
except :
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print (''.join('!! ' + line for line in lines))
    print("----------------------------")
    print(json.dumps(lines, indent=4, sort_keys=True))
    print("----------------------------")
    print (lines[len(lines) - 1])
#       
#     var = traceback.format_exc()
#     print (var)
#      
#     exc_type, exc_value, exc_tb = sys.exc_info()
#     traceback.print_exception(exc_type, exc_value, exc_tb)
#     print (exc_type)
#     print (exc_value)
#     print (exc_tb)
#
#     traceback.print_exc()
#     traceback.print_exc(limit=1, file=sys.stdout)
