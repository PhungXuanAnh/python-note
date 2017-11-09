'''
Created on Mar 30, 2017

@author: xuananh
'''

import shutil
import os
import errno
from os.path import basename
src = '/media/xuananh/data/Temp/Temp.py'
dst = '/media/xuananh/data'

from os.path import expanduser
home = expanduser("~")
print home

# shutil.copyfile(src, dst + '/' + basename(src))
# shutil.copy2(src, dst)
shutil.copy2(src, dst + '/temp1.txt')


'''
-------------------------------------------------------------------------
| Function          |Copies Metadata|Copies Permissions|Can Specify Buffer|
-------------------------------------------------------------------------
| shutil.copy       |      No       |        Yes       |        No        |
-------------------------------------------------------------------------
| shutil.copyfile   |      No       |         No       |        No        |
-------------------------------------------------------------------------
| shutil.copy2      |     Yes       |        Yes       |        No        |
-------------------------------------------------------------------------
| shutil.copyfileobj|      No       |         No       |       Yes        |
-------------------------------------------------------------------------

'''

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise     

# # rename file
os.rename('/media/xuananh/data/Temp/Temp2.py', '/media/xuananh/data/Temp/temp1111.py')
# # rename
# shutil.move('/media/xuananh/data/Temp/Temp2.py', '/media/xuananh/data/Temp/Temp1.py') 
# # move and rename
# shutil.move('/media/xuananh/data/Temp/Temp1.py', '/home/xuananh/Temp2.py')
# # just move
# shutil.move('/media/xuananh/data/Temp/Temp1.py', '/home/xuananh/')
