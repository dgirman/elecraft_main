import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication,QLabel,QMainWindow,QStackedLayout,QWidget,)

from layout_colorwidget import Color

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout = QStackedLayout()

        layout.addWidget(Color("red"))
        layout.addWidget(Color("blue"))
        layout.addWidget(Color("green"))
        layout.addWidget(Color("yellow"))

        layout.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()