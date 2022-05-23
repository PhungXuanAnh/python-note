import os
import zipfile
import logging
import datetime

path_to_zip_file = "/home/xuananh/data/Downloads/plugin/ping-nsb1.zip"
directory_to_extract_to = '/home/xuananh/data/Downloads'

def extractall(path_to_zip_file, directory_to_extract_to):
    try:
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()
        return True
    except:
        logging.exception("Error while extract file: " + path_to_zip_file)
        return False
    
def print_info(archive_name):
    print("Infor of archive file: ")
    zf = zipfile.ZipFile(archive_name)
    for info in zf.infolist():
        print(info.filename)
        print('\tComment:\t', info.comment)
        print('\tModified:\t', datetime.datetime(*info.date_time))
        print('\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)')
        print('\tZIP version:\t', info.create_version)
        print('\tCompressed:\t', info.compress_size, 'bytes')
        print('\tUncompressed:\t', info.file_size, 'bytes')


def retrieve_archive_member_info(archive_file, member_list):
    zf = zipfile.ZipFile(path_to_zip_file, 'r')    
    for filename in member_list:
        try:
            info = zf.getinfo(filename)
        except KeyError:
            print('ERROR: Did not find %s in zip file' % filename)
        else:
            print('%s is %d bytes' % (info.filename, info.file_size))



def zipfolder(the_name_of_the_zipfile="test_zipfile", 
              the_directory_to_be_zipped="/home/xuananh/repo/python-note/unittest_sample"):            
    # reference : https://stackoverflow.com/a/10480441/7639845
    zipobj = zipfile.ZipFile(the_name_of_the_zipfile + '.zip', 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(the_directory_to_be_zipped) + 1
    for base, dirs, files in os.walk(the_directory_to_be_zipped):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])

      
    
if __name__ == '__main__':
    # print("File is zip format: {}".format(zipfile.is_zipfile(path_to_zip_file)))

    # zf = zipfile.ZipFile(path_to_zip_file, 'r')    
    # print("Files name of the files in archive: {}".format(zf.namelist()))
    
    # print_info(path_to_zip_file)
    
    # retrieve_archive_member_info(path_to_zip_file, [ 'README.txt', 'ping.yaml', 'ping-nsb1/ping.py' ])
    
    zipfolder()
    