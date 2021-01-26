''' 
    NOTE: install packages before install pyaudio 

    On Ubuntu:
        sudo apt-get install python-pyaudio
        sudo apt-get install python3-pyaudio
    On MacOS:
        brew install portaudio
''' 

from urllib.request import urlopen
import pyaudio

pyaud = pyaudio.PyAudio()
srate=44100
stream = pyaud.open(format = pyaud.get_format_from_width(1),
                channels = 1,
                rate = srate,
                output = True)

url = 'http://mp3channels.webradio.antenne.de/chillout'
url = "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3"
u = urlopen(url)
data = u.read(8192)

while data:
    stream.write(data)
    data = u.read(8192)
