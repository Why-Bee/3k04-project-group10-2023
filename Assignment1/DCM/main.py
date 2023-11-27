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

    # Insert a PVARP column into AAI_data table and AAIR_data table with default value 250ms
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM all_users")
    users = c.fetchall()
    for user in users:
        c.execute("UPDATE AAI_data SET PVARP = ? WHERE id = ?", (250, user[2],))
        c.execute("UPDATE AAIR_data SET PVARP = ? WHERE id = ?", (250, user[2],))
        print("Updated user " + str(user[2]) + " with PVARP = 250ms")
    for user in users:
        c.execute("UPDATE AAI_data SET atrial_sensitivity = ? WHERE id = ?", (75, user[2],))
        c.execute("UPDATE AAIR_data SET atrial_sensitivity = ? WHERE id = ?", (75, user[2],))
        print("Updated user " + str(user[2]) + " with atrial_sensitivity = 0.75mV")
    conn.commit()
    conn.close()


    sys.exit(app.exec_()) 
