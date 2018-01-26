#!/usr/bin/python
import re

string = 'thanhtaittv9A'
string1 ='1231434'
string2 = 'abc'
match = re.match(r'T', string, re.IGNORECASE)
if match:
    print('match')
else:
    print('NOT match')