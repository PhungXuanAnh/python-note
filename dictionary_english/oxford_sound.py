#!/usr/bin/python
# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import json
import urllib2
import logging
import urlparse
import os
import sys
import pyglet

def get_word(app_id, app_key, language, word_id):
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
    return requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

def get_sound_url(response):
    response = response.json()
    return response["results"][0]["lexicalEntries"][0]["pronunciations"][0]["audioFile"]

def download(url):
    split = urlparse.urlsplit(url)
    filename = "/tmp/" + split.path.split("/")[-1]
    
    try:        
        f = urllib2.urlopen(url)
        data = f.read()
        with open(filename, "wb") as code:
            code.write(data)
            
        return filename
    except:
        logging.exception("Downloading error 2: ")
        return None

def play(file_path):
    song = pyglet.media.load(file_path)
    song.play()
    
    def exiter(dt):
        pyglet.app.exit()
    print "Song length is: %f" % song.duration
    # song.duration is the song length
    pyglet.clock.schedule_once(exiter, song.duration)
    
    pyglet.app.run()
    
if __name__ == '__main__':
    # TODO: replace with your own app_id and app_key
    app_id = 'e79fcf4a'
    app_key = 'e3d7845cb77a112ca2685d095c61a71d'
    language = 'en'
    word_id = sys.argv[1]

    response = get_word(app_id, app_key, language, word_id)
    # print("code {}\n".format(r.status_code))
    # print("text \n" + r.text)
    # print("json \n" + json.dumps(r.json(), indent=4, sort_keys=True))
    url = get_sound_url(response)
    file_path = download(url)
    play(file_path)
    os.remove(file_path)
        
