import sys

from PyQt5.QtWidgets import QApplication, QStackedWidget

from windows.welcome.welcome import MyWindow

from fill_database import fill_database
from empty_database import empty_database

import sqlite3


if __name__ == '__main__':
    app = QApplication(sys.argv) # create application
    stacked_window = QStackedWidget() # create stacked widget
    window = MyWindow(stacked_window) # create welcome screen
    stacked_window.addWidget(window) # add welcome screen to stacked widget
    stacked_window.setFixedWidth(1200) # set fixed width and height
    stacked_window.setFixedHeight(800)
    stacked_window.show()

    # TEST FUNCTIONS
    # empty_database() # empty database except for admin user
    # fill_database() # fill database


    sys.exit(app.exec_()) 
