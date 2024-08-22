from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

if __name__ == '__main__':
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QApplication, QMainWindow
    import sys
    class MainWindow(QMainWindow):
        def __init__(self):

            super().__init__()
            self.setWindowTitle("My App")
            widget = Color("red")
            self.setCentralWidget(widget)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
