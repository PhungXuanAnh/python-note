import logging
from urllib.parse import urlparse
from urllib.request import urlopen, urlretrieve
import requests


def get_file_name(save_folder, url):
    split = urlparse(url)
    filename = save_folder + '/' + split.path.split("/")[-1]
    print(filename)
    return filename


def download_by_urllib_urlretrieve(save_folder, url):
    try:
        urlretrieve(url, get_file_name(save_folder, url))
    except:
        logging.exception("Downloading error 1: ")  

def download_by_urllib_urlopen(save_folder, url):
    try:        
        f = urlopen(url)
        data = f.read()
        with open(get_file_name(save_folder, url), "wb") as code:
            code.write(data)
    except:
        logging.exception("Downloading error 2: ")  

def download_by_requests(save_folder, url):
    try:        
        r = requests.get(url)
        with open(get_file_name(save_folder, url), "wb") as code:
            code.write(r.content)
    except:
        logging.exception("Downloading error 3: ")


if __name__ == "__main__":

    # url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip1'
    # url = 'https://www.dropbox.com/s/41ti4o4x8zzz8y8/Backup-codes-phungxuananh.bk.txt?dl=1'
    # url = 'https://uec-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img'
    url = "https://scontent.fhan3-1.fna.fbcdn.net/v/t1.6435-9/s851x315/114384286_2591158021201514_4156760717270136191_n.jpg?_nc_cat=110&ccb=1-3&_nc_sid=da31f3&_nc_ohc=BMeg_z4XW_EAX_0ypl2&_nc_ht=scontent.fhan3-1.fna&tp=7&oh=25c883acd88471d6d7dfa181a419a118&oe=60C667C0"
    save_folder = '/home/xuananh/Downloads'    

    # download_by_urllib_urlopen(save_folder, url)
    download_by_urllib_urlretrieve(save_folder, url)
    # download_by_requests(save_folder, url)


