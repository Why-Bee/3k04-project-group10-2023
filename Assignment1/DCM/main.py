import sys

from PyQt5.QtWidgets import QApplication, QStackedWidget

from windows.welcome.welcome import MyWindow

from fill_database import fill_database
from empty_database import empty_database


TESTING = True # set to True to empty and fill database


if __name__ == '__main__':
    app = QApplication(sys.argv) # create application
    stacked_window = QStackedWidget() # create stacked widget
    window = MyWindow(stacked_window) # create welcome screen
    stacked_window.addWidget(window) # add welcome screen to stacked widget
    stacked_window.setFixedWidth(1200) # set fixed width and height
    stacked_window.setFixedHeight(800)
    stacked_window.show()

    # TEST FUNCTIONS
    # do NOT use in first run with new modes / parameters
    if TESTING:
        empty_database() # empty database except for admin user
        fill_database() # fill database with test data
        print("Tests successful")


    sys.exit(app.exec_()) 
