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

        extractAction = QtGui.QAction("&GET TO THE CHOPPAH!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        

        self.home() # button method, define ui and functionality

    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(0,100)

        extractAction = QtGui.QAction(QtGui.QIcon('todachoppa.png'), 'Flee the Scene', self)
        extractAction.triggered.connect(self.close_application)
        
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)
 
        self.show()

    def close_application(self):
        choice = QtGui.QMessageBox.question(                                                # This is a pre-made message box window that comes with PyQT.
                                            self, 
                                            'Extract!',                                     # window title
                                            "Get into the chopper?",                        # window message
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
                                            | QtGui.QMessageBox.Cancel)   # Here, the | denotes an either-or situation. Only one can be chosen.
        
        if choice == QtGui.QMessageBox.Yes:                 # checks to see what the user picked
            print("Extracting Naaaaaaoooww!!!!")
            sys.exit()
        else:
            pass

    
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()