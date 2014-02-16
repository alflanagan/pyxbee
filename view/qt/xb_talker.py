#!/usr/bin/python
# vim: fileencoding=utf-8

# Import PySide classes
import sys
from PySide.QtCore import *
from PySide.QtGui import *


if __name__ == "__main__":
    # Create a Qt application
    app = QApplication(sys.argv)
    # Create a Label and show it
    label = QLabel("Hello World")
    label.show()
    # Enter Qt application main loop
    app.exec_()
    sys.exit()
