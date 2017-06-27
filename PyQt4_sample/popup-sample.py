'''
Created on Jun 26, 2017

@author: xuananh
'''
# Necessary imports

from PyQt4 import QtGui
import sys

class MyPopupDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        # Regular init stuff...
        # and other things you might want
        pass


class MyForm(QtGui.QDialog):
    def __init__(self, parent=None):
        # Here, you should call the inherited class' init, which is QDialog
        QtGui.QDialog.__init__(self, parent)
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.home()
        
        def home(self):
            '''method definition create button object'''
            btn = QtGui.QPushButton("Quit", self)                           # with text that says quit.
            btn.clicked.connect(self.popup())    # Define what to do when button is clicked
            btn.resize(100,100)                                             # Define what to do when button is clicked
            btn.move(100,100)                                               # Move button placement
            self.show()    


    def popup(self):
        self.dialog = MyPopupDialog()

        # For Modal dialogs
        self.dialog.exec_()

        # Or for modeless dialogs
        # self.dialog.show()

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   myapp= MyForm()
   myapp.show()
   sys.exit(app.exec_())