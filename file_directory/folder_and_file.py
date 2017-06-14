import os
import shutil

# Find out current working directory #
script_dir = os.path.dirname(__file__)
print script_dir

dir_path = os.path.dirname(os.path.realpath(__file__))
print dir_path

current_working_dir = os.getcwd()
print current_working_dir

# Check folder exist? If not creat it #
if not os.path.exists('/media/xuananh/data/Temp/test1/test2'):
    os.makedirs('/media/xuananh/data/Temp/test1/test2')
   
# Check file or folder exist? 
if os.path.exists('test_dir'):
    print "File is exist"
else :
    print "File is NOT exist"
    
# Check file exist
print (os.path.isfile("path"))
print (not os.path.isfile("path"))
    
# remove a file. #
os.remove("path")     
# remove an empty directory. #
os.rmdir('test_dir')
# delete a directory and all its contents. #      
shutil.rmtree("path") 