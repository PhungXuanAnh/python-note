'''
Created on Jun 26, 2017

@author: xuananh

app = QtGui.QApplication(sys.argv)        --> Define the App.
GUI = Window()                            --> Define the GUI (.show() will hide in here)
sys.exit(app.exec_())                     --> Run some simple exit code to ensure clean exit

'''

import sys
from PyQt4 import QtGui

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.show()

app = QtGui.QApplication(sys.argv)      # --> Define the App.
GUI = Window()                          # --> Define the GUI (.show() will hide in here)
sys.exit(app.exec_())                   # --> Run some simple exit code to ensure clean exit