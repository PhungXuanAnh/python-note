import sys
from PyQt4 import QtCore, QtGui

class Example(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.label = QtGui.QLabel(self)
        self.label.resize(500, 100)
        font_label = QtGui.QFont()
        font_label.setPointSize(75);
        font_label.setBold(True);
        self.label.setFont(font_label)
        
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        
        self._text = 'this is a test'
        self._index = 0
        
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.handleTimer)
        self.timer.start(200)

    def handleTimer(self):
        self._index += 1
        self.label.setText(self._text[:self._index])
        if self._index > len(self._text):
            self.timer.stop()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.setGeometry(300, 300, 250, 150)
    ex.show()
    sys.exit(app.exec_())