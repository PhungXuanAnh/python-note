import zipfile
import logging

path_to_zip_file = '/media/xuananh/data/Downloads/codes.zip'
directory_to_extract_to = '/media/xuananh/data/Downloads/code_zip'

try:
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
except:
    logging.exception("Error while extract file: " + path_to_zip_file)    

# zip = zipfile.ZipFile(r'c:\my.zip')  
# zip.extractall(r'c:\output')  