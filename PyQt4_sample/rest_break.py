import sys
import pyglet
from PyQt4 import QtCore
from PyQt4 import QtGui

def play_song(song_file):   
    song = pyglet.media.load(song_file)
    song.play()
     
    def exiter(dt):
        pyglet.app.exit()
    print "Song length is: %f" % song.duration
    # song.duration is the song length
    pyglet.clock.schedule_once(exiter, song.duration)
     
    pyglet.app.run()

class TimerMessageBox(QtGui.QMessageBox):
    def __init__(self, timeout=3, parent=None):
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle("wait")
        self.time_to_wait = timeout
        self.setText("wait (closing automatically in {0} secondes.)".format(timeout))
        self.setStandardButtons(QtGui.QMessageBox.Cancel)
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()
        self.activateWindow()
        self.raise_()
        play_song('/media/xuananh/data/Downloads/Saved/.music/Fantasy-magical-sound-effect.mp3')
        
    def changeContent(self):
        self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            event.accept()
        else:
            super(TimerMessageBox, self).keyPressEvent(event)
            
    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QtGui.QCursor.pos())
        self.setGeometry(geom)
        super(TimerMessageBox, self).showEvent(event)
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.setTopLevelWindow()
            self.dialog.close()

            return True

        return False
        
    def setTopLevelWindow(self):    
        if self.windowState() != QtCore.Qt.WindowMaximized:
            self.showMaximized()
            self.showNormal()

        else:
            self.showNormal()
            self.showMaximized()

        self.raise_()
        self.activateWindow()
     
class Example(QtGui.QMainWindow):
    
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.TIME_BREAK = 1200
        self.time_rest_break = self.TIME_BREAK
        print("time rest break = {}".format(self.time_rest_break))
        
        self.label = QtGui.QLabel(self)
        self.label.resize(500, 100)
        font_label = QtGui.QFont()
        font_label.setPointSize(75);
        font_label.setBold(True);
        self.label.setFont(font_label)
        
        self.btn = QtGui.QPushButton('Set time', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(1, 110)
        self.btn.resize(200,100)
        self.btn.clicked.connect(self.btn_function)
        
#         self.textEdit = QtGui.QTextEdit(self)
#         self.textEdit.move(210, 110)
#         self.textEdit.resize(100, 50)
        
        self.textbox = QtGui.QLineEdit(self)
        self.textbox.move(210, 110)
        self.textbox.resize(100, 50)
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.warning)
        self.timer.start()
        
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(50, 50, 500, 300)
        

    def warning(self):
        self.time_rest_break -= 1
        
        m, s = divmod(self.time_rest_break, 60)
        h, m = divmod(m, 60)
        self.label.setText("%d:%02d:%02d" % (h, m, s))
        print("time rest break = {} = {}:{:02d}:{:02d}".format(self.time_rest_break, h, m, s))
        
        if self.time_rest_break <= 0:
            self.time_rest_break = 2  
            messagebox = TimerMessageBox(3, self)
            messagebox.exec_()
            if messagebox.clickedButton() != None:
                self.time_rest_break = self.TIME_BREAK
                
    def btn_function(self):
        self.TIME_BREAK = int(self.textbox.text()) * 60
        self.time_rest_break = int(self.textbox.text()) * 60
                
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()