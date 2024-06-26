import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

import call_pipeline


class IconButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.pix = QPixmap('gui/icons/pngwing.com.png')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pix)

    def sizeHint(self):
        return QSize(500, 500)


app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Mockup Callcenter")
window.setFixedSize(500, 500)  # Set the dimensions of the window.

button = IconButton()
button.clicked.connect(call_pipeline.respond_to_caller)

windowLayout = QVBoxLayout()
windowLayout.addWidget(button)

central_widget = QWidget()
central_widget.setLayout(windowLayout)
window.setCentralWidget(central_widget)

window.show()

sys.exit(app.exec())
