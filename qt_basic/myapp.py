import sys, os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QApplication,
                QHBoxLayout, QLabel,  QMainWindow, QPushButton,QStackedLayout,
                QVBoxLayout, QWidget, QToolBar, QStatusBar
                )
from PyQt6.QtGui import QAction, QIcon
from layout_colorwidget import Color

basedir = os.path.dirname(__file__)

# tag::MainWindow[]
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(
            QIcon("bug.png"),
            "Your button",
            self,
        )

        button_action = QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self, s):
        print("click", s)

# end::MainWindow[]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
