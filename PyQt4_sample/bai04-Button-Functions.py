'''
Created on Jun 26, 2017

@author: xuananh
'''
import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.home()

    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())           # return what QT thinks is the smallest reasonable size for your button.
                                                    # or can use sizeHint() will return what QT thinks is the best side for our button.
        btn.move(0,0)
        self.show()

    def close_application(self):                # ---> define our function for button
        print("whooaaaa so custom!!!")          # print to console
        sys.exit()                              # exit app
    
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()