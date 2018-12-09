import time
import os
import shutil

# Find out current working directory #
script_dir = os.path.dirname(__file__)
print (script_dir)

dir_path = os.path.dirname(os.path.realpath(__file__))
print (dir_path)

current_working_dir = os.getcwd()
print (current_working_dir)

# Check file or folder exist?
if os.path.exists('test_dir'):
    print ("File is exist")
else:
    print ("File is NOT exist")

# Check file exist
print (os.path.isfile("path"))
print (not os.path.isfile("path"))

# Check folder exist? If not creat it #
if not os.path.exists('/home/xuananh/data/Temp/test1/test2'):
    os.makedirs('/home/xuananh/data/Temp/test1/test2')

time.sleep(5)
try:
    # remove a file. #
    os.remove("/home/xuananh/data/Temp/test1")
except Exception as e:
    print('111111111111 ', e)
    print (e)

try:
    # remove an empty directory. #
    os.rmdir('/home/xuananh/data/Temp/test1')
except Exception as e:
    print('22222222222222 ', e)

try:
    # delete a directory and all its contents. #
    shutil.rmtree("/home/xuananh/data/Temp/test1")
except Exception as e:
    print('333333333333333 ', e)        

print (os.getcwd())
print (os.path.exists("../abc_module"))
print (os.path.join("a", "b", "c"))
