import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QStackedWidget

from sqlite3 import connect
from hashlib import sha256

from windows.welcome.welcome import MyWindow


id = 0 # id of user


if __name__ == '__main__':
    app = QApplication(sys.argv) # create application
    stacked_window = QStackedWidget() # create stacked widget
    window = MyWindow(stacked_window) # create welcome screen
    stacked_window.addWidget(window) # add welcome screen to stacked widget
    stacked_window.setFixedWidth(1200) # set fixed width and height
    stacked_window.setFixedHeight(800)
    stacked_window.show()

    sys.exit(app.exec_()) 

