import sys
import random
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt

from MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        f = self.label.font()
        f.setPointSize(25)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter
            | Qt.AlignmentFlag.AlignVCenter)

        self.label.setFont(f)
        self.pushButton.pressed.connect(self.update_label)

        # Signals from UI widgets can be connected as normal. self.pushButton.pressed.connect(self.update_label)

    def update_label(self):
        n = random.randint(1, 6)
        self.label.setText("%d" % n)



app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()