#!/usr/bin/python

import sys
import json
import os
import pyglet

# success

def find_all(name, path):
    print (name, path)
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def find_all_sound(name, sound_dir):
    
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
    print "Song length is: %f" % song.duration
    # song.duration is the song length
    pyglet.clock.schedule_once(exiter, song.duration)
    
    pyglet.app.run()
    
if __name__ == '__main__':
#     print 'Number of arguments:', len(sys.argv), 'arguments.'
#     print 'Argument List:'
#     print (json.dumps(sys.argv, indent=4, sort_keys=True))
#     print ("sys.argv[1] = {} \n sys.argv[2] = {}"\
#            .format(sys.argv[1], sys.argv[2]))
    
#     sound_dir = '/home/xuananh/.goldendict/Longman-2005-Voice-Package-British'

    ''' Note: play_sound_goldendict.py [word] [sound_dir] '''
    
    result = []
    result = find_all_sound(sys.argv[1], sys.argv[2])
    print result
    
    for file_path in result:
        play(file_path)
        