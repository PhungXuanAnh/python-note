import os

current_dir = os.path.dirname(__file__)
song_file = current_dir + "/test.mp3"
def play_mp3():
    """
        NOTE: to install package playsound on ubuntu, install following packages in advance:

        on ubuntu:
            sudo apt-get update && sudo apt-get upgrade -y
            sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python-dev gir1.2-gtk-3.0
            pip install pycairo
            pip install PyGObject

        on OSX:
            brew install pkg-config
            brew install cairo

        then: 
            pip install -r requirements.txt
    """
    import playsound
    playsound.playsound(song_file, True)

if __name__ == "__main__":
    play_mp3()
