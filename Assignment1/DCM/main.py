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
    empty_database() # empty database except for admin user
    fill_database() # fill database

    # Insert a ventricular_sensitivity column into VVI_data, and VVIR_data tables with default value 2.5mV
    # conn = sqlite3.connect('users.db')
    # c = conn.cursor()
    # c.execute("SELECT * FROM all_users")
    # users = c.fetchall()
    
    # conn.commit()
    # conn.close()


    sys.exit(app.exec_()) 
