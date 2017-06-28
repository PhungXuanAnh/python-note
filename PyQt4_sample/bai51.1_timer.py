import sys

# from PyQt4.QtCore import QTimer
# from PyQt4.QtGui import QApplication
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Dialog(QDialog):

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.resize(300,200)

    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QCursor.pos())
        self.setGeometry(geom)
        super(Dialog, self).showEvent(event)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
            event.accept()
        else:
            super(Dialog, self).keyPressEvent(event)
            
def showdialog():
    d = Dialog()
    
    b1 = QPushButton("ok Dialog",d)
    b1.move(50,50)
    
    d.setWindowTitle("Dialog")
    d.setWindowModality(Qt.ApplicationModal)
    d.exec_()
    
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

timer = QTimer()
timer.timeout.connect(showdialog)
timer.start(1000)

# run event loop so python doesn't exit
app.exec_()


