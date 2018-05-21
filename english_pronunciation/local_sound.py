#!/usr/bin/python
# sudo -H pip install requests
# sudo -H pip install pyglet
# install AVbin: Download here: http://avbin.github.io/AVbin/Download.html
# wget https://github.com/downloads/AVbin/AVbin/install-avbin-linux-x86-64-v10
# chmod +x install-avbin-linux-x86-64-v10
# Sudo ./install-avbin-linux-x86-64-v10

import sys
import json
import os
import pyglet
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S", 
#     stream=sys.stdout,
    filename="/tmp/local_sound.log",
    )
def find_all(name, path):
    logging.info('Looking file {} in path {} '.format(name, path))
    result = []
    for root, _, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def find_all_sound_file(name, sound_dir):
    
    # find in upper character directory
    result = find_all(name + '.mp3', sound_dir + '/' + name[0].upper())
    if result:
        return result
    
    result = find_all(name.upper() + '.mp3', sound_dir + '/' + name[0].upper())
    if result:
        return result
    
    result = find_all(name.lower() + '.mp3', sound_dir + '/' + name[0].upper())
    if result:
        return result
    
    # find in lower character directory
    result = find_all(name + '.mp3', sound_dir + '/' + name[0].lower())
    if result:
        return result
    
    result = find_all(name.upper() + '.mp3', sound_dir + '/' + name[0].lower())
    if result:
        return result
    
    result = find_all(name.lower() + '.mp3', sound_dir + '/' + name[0].lower())
    if result:
        return result
    
    # find in other directory
    result = find_all(name + '.mp3', sound_dir + '/other')
    if result:
        return result
    
    result = find_all(name.upper() + '.mp3', sound_dir + '/other')
    if result:
        return result
    
    result = find_all(name.lower() + '.mp3', sound_dir + '/other')
    if result:
        return result    
    
    
    # find in 0-9 directory
    result = find_all(name + '.mp3', sound_dir + '/0-9')
    if result:
        return result
    
    result = find_all(name.upper() + '.mp3', sound_dir + '/0-9')
    if result:
        return result
    
    result = find_all(name.lower() + '.mp3', sound_dir + '/0-9')
    if result:
        return result
        
def play(file_path):
    song = pyglet.media.load(file_path)
    song.play()
    
    def exiter(dt):
        pyglet.app.exit()
    logging.info("Song length is: %f" % song.duration)
    # song.duration is the song length
    pyglet.clock.schedule_once(exiter, song.duration)
    
    pyglet.app.run()
    
if __name__ == '__main__':
#     logging.info 'Number of arguments:', len(sys.argv), 'arguments.'
#     logging.info 'Argument List:'
#     logging.info (json.dumps(sys.argv, indent=4, sort_keys=True))
#     logging.info ("sys.argv[1] = {} \n sys.argv[2] = {}"\
#            .format(sys.argv[1], sys.argv[2]))
    
    ''' 
Usage: 
    local_sound.py [word] [sound_dir] 

    python2-env /media/xuananh/data/github/python-note/english_pronunciation/local_sound.py %GDWORD% /media/xuananh/data/.goldendict/Webster-Voice-Package-English

'''
    
    result = []
    result = find_all_sound_file(name=sys.argv[1], sound_dir=sys.argv[2])
    logging.info(result)
    
    if result != None:
        for file_path in result:
            play(file_path)
        