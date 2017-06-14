''' sudo apt-get install python-pyaudio
    sudo apt-get install python3-pyaudio
    chay re re, eo hieu luon
''' 

from urllib2 import urlopen
# from urllib.request import urlopen
import pyaudio

pyaud = pyaudio.PyAudio()
srate=44100
stream = pyaud.open(format = pyaud.get_format_from_width(1),
                channels = 1,
                rate = srate,
                output = True)

# url = 'http://audio.oxforddictionaries.com/en/mp3/ace_gb_1.mp3'
# url = "http://download.wavetlan.com/SVV/Media/HTTP/WAV/NeroSoundTrax/NeroSoundTrax_test4_PCM_Mono_VBR_8SS_44100Hz.wav"
url = 'http://mp3channels.webradio.antenne.de/chillout'
u = urlopen(url)
data = u.read(8192)

while data:
    stream.write(data)
    data = u.read(8192)