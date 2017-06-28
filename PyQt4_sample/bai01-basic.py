from PyQt4 import QtGui
import sys
  
# class HelloPython(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(HelloPython, self).__init__(parent)
#         helloLabel = QtGui.QLabel("Say Hello To PyQT!")       
#         helloLineEdit = QtGui.QLineEdit()
#   
#         mainLayout = QtGui.QGridLayout()
#         mainLayout.addWidget(helloLabel, 0, 0)
#         mainLayout.addWidget(helloLineEdit, 0, 1)
#   
#         self.setLayout(mainLayout)
#         self.setWindowTitle("My Python App")
#   
# if __name__ == '__main__':
#   
#     app = QtGui.QApplication(sys.argv)
#   
#     helloPythonWidget = HelloPython()
#     helloPythonWidget.show()
#   
#     sys.exit(app.exec_())

import sys
from PyQt4 import QtGui
 
app = QtGui.QApplication(sys.argv)
 
window = QtGui.QWidget()
 
window.setGeometry(0, 0, 500, 300)
 
window.setWindowTitle("PyQT Tuts!")
 
window.show()
 
sys.exit(app.exec_())