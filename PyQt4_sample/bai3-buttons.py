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
        '''method definition create button object'''
        btn = QtGui.QPushButton("Quit", self)                           # with text that says quit.
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)    # Define what to do when button is clicked
        btn.resize(100,100)                                             # Define what to do when button is clicked
        btn.move(100,100)                                               # Move button placement
        self.show()                                                     # Show Window.

        
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()