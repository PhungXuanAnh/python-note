"""
Transcript - direct print output to a file, in addition to terminal.

Usage:
    import transcript
    transcript.start('logfile.log')
    print("inside file")
    transcript.stop()
    print("outside file")
"""

import sys

class Transcript(object):

    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass

def start(filename):
    """Start transcript, appending print output to given filename"""
    sys.stdout = Transcript(filename)

def stop():
    """Stop transcript and return print functionality to normal"""
    sys.stdout.logfile.close()
    sys.stdout = sys.stdout.terminal
    
    
if __name__ == '__main__':
    start('logs_file.out2')
    print("inside file")
    stop()
    print("outside file")    