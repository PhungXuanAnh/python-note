song_file = "/media/xuananh/data/Downloads/.music/Magic-chimes.mp3"

''' to use pyglet with compressed audio as mp3, need to install AVbin ============== GOOD
    Download here: http://avbin.github.io/AVbin/Download.html '''
import pyglet    
song = pyglet.media.load(song_file)
song.play()
    
def exiter(dt):
    pyglet.app.exit()
print ("Song length is: %f" % song.duration)
# song.duration is the song length
pyglet.clock.schedule_once(exiter, song.duration)
    
pyglet.app.run()


'''
pygame is not stable when play multi time with very short song like indent.mp3
but it is very good with long song like a.mp3   
'''
# import pygame
# pygame.mixer.init()
# pygame.mixer.music.load(song_file)
# pygame.mixer.music.play()
# while pygame.mixer.music.get_busy() == True:
#     continue
# pygame.mixer.quit()


''' tham khao thoi, khong play dc
    sudo apt-get install python-gst0.10 
    sudo apt-get install gstreamer0.10-plugins-good 
    sudo apt-get install gstreamer0.10-alsa'''
# import pygst
# pygst.require('0.10')
# import gst
# import gobject
# mainloop = gobject.MainLoop()
# pl = gst.element_factory_make("playbin", "player")
# pl.set_property('uri', song_file1)
# pl.set_state(gst.STATE_PLAYING)
# mainloop.run()

