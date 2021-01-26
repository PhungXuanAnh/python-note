import os

current_dir = os.path.dirname(__file__)
song_file = current_dir + "/test.mp3"
def play_mp3():
    import playsound
    playsound.playsound(song_file, True)

if __name__ == "__main__":
    play_mp3()
