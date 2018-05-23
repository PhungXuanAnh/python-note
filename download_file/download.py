import urllib
import urllib2
import requests
import logging
import urlparse

'''
Note: co 3 cach de tai file
       cach dung urllib va request van download va save file khi link bi loi, va khong bao loi
       cach dung urllib2 khong download va save khi link bi loi va se bao loi

'''

url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip1'
# url = 'https://www.dropbox.com/s/41ti4o4x8zzz8y8/Backup-codes-phungxuananh.bk.txt?dl=1'
# url = 'https://uec-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img'

# get file name from url #
split = urlparse.urlsplit(url)
filename = "/media/xuananh/data/Downloads/" + split.path.split("/")[-1]

print (filename)

# Cach 1:  time download: 02.03.08 #
try:
    print ("downloading with urllib")
    urllib.urlretrieve(url, filename)
except:
    logging.exception("Downloading error 1: ")  

# Cach 2: time download: 01.42.49 #
try:        
    print ("downloading with urllib2")
    f = urllib2.urlopen(url)
    data = f.read()
    with open(filename, "wb") as code:
        code.write(data)
except:
    logging.exception("Downloading error 2: ")  

# Cach 3: time download: 01.44.47 #
try:        
    print ("downloading with requests")
    r = requests.get(url)
    with open(filename, "wb") as code:
        code.write(r.content)
except:
    logging.exception("Downloading error 3: ")           