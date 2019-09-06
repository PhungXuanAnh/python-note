'''
Created on Jun 23, 2017

@author: xuananh
'''
import json

def check_line_is_comment(line):
    pass

file_name = '/media/xuananh/data/Temp/20authentication.conf'
file_name1 = '/media/xuananh/data/Temp/out.conf'

def remove_c_comment(file_name):
    ''' remove comment // in json file'''
    json_string = ''
    with open(file_name, 'r') as f:
        for line in f:
            
            print(line)
            
            check_ahead = False
            temp_line = ''
            for charac in line:
                if charac == '/':
                    if check_ahead:
                        temp_line = temp_line + '\n'
                        break
                    else:
                        check_ahead = True
                else:
                    if check_ahead:
                        temp_line = temp_line + '/'
                        
                    check_ahead = False
                    temp_line = temp_line + charac
                    
            json_string = json_string + temp_line
            
    print(json_string)
                
    with open(file_name, 'w+') as f:
        f.write(json_string)