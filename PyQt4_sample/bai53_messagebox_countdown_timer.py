from PyQt4.QtGui import QMessageBox as MBox, QApplication
from PyQt4.QtCore import QTimer


class TimedMBox(MBox):
    """
    Variant of QMessageBox that automatically clicks the default button
    after the timeout is elapsed
    """
    def __init__(self, timeout=5, buttons=None, **kwargs):
        if not buttons:
            buttons = [MBox.Retry, MBox.Abort, MBox.Cancel]

        self.timer = QTimer()
        self.timeout = timeout
        self.timer.timeout.connect(self.tick)
        self.timer.setInterval(1000)
        super(TimedMBox, self).__init__(parent=None)

        if "text" in kwargs:
            self.setText(kwargs["text"])
        if "title" in kwargs:
            self.setWindowTitle(kwargs["title"])
        self.t_btn = self.addButton(buttons.pop(0))
        self.t_btn_text = self.t_btn.text()
        self.setDefaultButton(self.t_btn)
        for button in buttons:
            self.addButton(button)

    def showEvent(self, e):
        super(TimedMBox, self).showEvent(e)
        self.tick()
        self.timer.start()

    def tick(self):
        self.timeout -= 1
        if self.timeout >= 0:
            self.t_btn.setText(self.t_btn_text + " (%i)" % self.timeout)
        else:
            self.timer.stop()
            self.defaultButton().animateClick()

    @staticmethod
    def question(**kwargs):
        """
        Ask user a question, which has a default answer. The default answer is
        automatically selected after a timeout.

        Parameters
        ----------

        title : string
            Title of the question window

        text : string
            Textual message to the user

        timeout : float
            Number of seconds before the default button is pressed

        buttons : {MBox.DefaultButton, array}
            Array of buttons for the dialog, default button first

        Returns
        -------
        button : MBox.DefaultButton
            The button that has been pressed
        """
        w = TimedMBox(**kwargs)
        w.setIcon(MBox.Question)
        return w.exec_()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = TimedMBox.question(text="Please select something",
                           title="Timed Message Box",
                           timeout=8)
    if w == MBox.Retry:
        print "Retry"
    if w == MBox.Cancel:
        print "Cancel"
    if w == MBox.Abort:
        print "Abort"
