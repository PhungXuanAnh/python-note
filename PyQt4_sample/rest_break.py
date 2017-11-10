import sys
import pyglet
from PyQt4 import QtCore
from PyQt4 import QtGui
import threading
import logging
import subprocess

def is_screen_locked():
    command = "gdbus call -e -d com.canonical.Unity -o /com/canonical/Unity/Session -m com.canonical.Unity.Session.IsLocked"
    process = subprocess.Popen(command, shell=True, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    result = process.communicate()
    
    if result[0] == '(true,)\n':
        return True
    elif result[0] == '(false,)\n':
        return False
    
class TimerMessageBox(QtGui.QMessageBox):
    def __init__(self, counter_show_in_messagebox, timeout=3, parent=None):
        super(TimerMessageBox, self).__init__(parent)
        
        self.counter_show_in_messagebox = counter_show_in_messagebox
        
        self.setWindowTitle("wait")
        self.time_to_wait = timeout
        self.setText("Show {} times. Closing in {} seconds".format(self.counter_show_in_messagebox, timeout))
        self.setStandardButtons(QtGui.QMessageBox.Cancel)
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()
        self.activateWindow()
        self.raise_()
        
    def changeContent(self):
        self.setText("Show {} times. Closing in {} seconds".format(self.counter_show_in_messagebox, self.time_to_wait))
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
        
        self.counter_show_in_messagebox = 0
        
        self.is_playing = False
        self.song_file = "/media/xuananh/data/Downloads/.music/Magic-chimes.mp3"
        
        self.TIME_BREAK = 1200
        self.time_rest_break = self.TIME_BREAK
        print("time rest break = {}".format(self.time_rest_break))
        
        self.label = QtGui.QLabel(self)
        self.label.resize(200, 50)
        font_label = QtGui.QFont()
        font_label.setPointSize(25);
        font_label.setBold(True);
        self.label.setFont(font_label)
        
        self.btn_settime = QtGui.QPushButton('Set time', self)
        self.btn_settime.resize(self.btn_settime.sizeHint())
        self.btn_settime.move(1, 110)
#         self.btn_settime.resize(100,50)   # wide = 200, high = 100
        self.btn_settime.clicked.connect(self.btn_func_settime)
        
        self.btn_reset = QtGui.QPushButton('Reset', self)
        self.btn_reset.resize(self.btn_reset.sizeHint())
        self.btn_reset.move(1, 150)     # column = 1, row =  150
#         self.btn_reset.resize(200,100)
        self.btn_reset.clicked.connect(self.btn_func_reset)
        
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
        self.setGeometry(50, 50, 350, 200)
        

    def warning(self):
        if is_screen_locked():
            self.time_rest_break = self.TIME_BREAK
            return
            
        self.time_rest_break -= 1
        
        m, s = divmod(self.time_rest_break, 60)
        h, m = divmod(m, 60)
        self.label.setText("%d:%02d:%02d" % (h, m, s))
        print("time rest break = {} = {}:{:02d}:{:02d}".format(self.time_rest_break, h, m, s))
        
        # if time rest break happend
        if self.time_rest_break <= 0:
            
            self.counter_show_in_messagebox += 1
            
            # play mp3 file
            if not self.is_playing:
                f2 = threading.Thread(target=self.play_song, args=[self.song_file])
                f2.start()
                
            self.time_rest_break = 2  
            # show message box
            messagebox = TimerMessageBox(self.counter_show_in_messagebox, 3, self)
            messagebox.exec_()
            
            # auto lock screen after 3 seconds
#             if self.counter_show_in_messagebox == 1:
            subprocess.Popen("gnome-screensaver-command -l", shell=True, 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.STDOUT)
            
            # when user click to Cancel button
            if messagebox.clickedButton() != None:
                if self.TIME_BREAK < 5:
                    self.TIME_BREAK = 1200
                self.time_rest_break = self.TIME_BREAK
                self.is_playing = False
#                 self.counter_show_in_messagebox = 0
                
    def btn_func_settime(self):
        self.TIME_BREAK = int(self.textbox.text()) * 60
        self.time_rest_break = self.TIME_BREAK
        
    def btn_func_reset(self):
        self.TIME_BREAK = 1200
        self.time_rest_break = self.TIME_BREAK
        
    def play_song(self, song_file):
        self.is_playing = True
        
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(song_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True and self.is_playing == True:
            continue
        
        self.is_playing = False
        pygame.mixer.quit()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
        
    