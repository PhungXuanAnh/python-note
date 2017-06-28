import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

time_rest_break = 1200

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
     
class Example(QtGui.QWidget):
    
    
    def __init__(self):
        super(Example, self).__init__()
        print("time rest breack = {}".format(time_rest_break))
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.warning)
        self.timer.start()
        
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        

    def warning(self):
        global time_rest_break
        print("time rest breack = {}".format(time_rest_break))
        time_rest_break -= 1
        if time_rest_break <= 0:
            time_rest_break = 2  
            messagebox = TimerMessageBox(5, self)
            messagebox.exec_()
            if messagebox.clickedButton() != None:
                time_rest_break = 1200
                
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()