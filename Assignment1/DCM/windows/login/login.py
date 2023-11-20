from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

from sqlite3 import connect
from hashlib import sha256

from windows.landingpage.landingpage import LandingWindow



class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi('./windows/login/login.ui', self)
        self.setWindowTitle('Login')
        self.backButton.clicked.connect(self.back_clicked)
        self.loginConfirm.clicked.connect(self.check_login)


    def back_clicked(self): # if back button is clicked, go back to welcome screen
        stacked_window.setCurrentIndex(0)
        # clear stack
        stacked_window.removeWidget(stacked_window.widget(1))

    def check_login(self):
        username = self.usernameField.text() # get username and password from text fields
        password = self.passwordField.text()
       
        if (len(username) == 0 or len(password) == 0): # check if fields are empty
            self.errorLabel.setText('Please fill in all fields')
        else:
            conn = connect('users.db') # connect to database
            c = conn.cursor()
            # check if only username is in database
            c.execute('SELECT * FROM all_users WHERE username=?', (username,))
            if (c.fetchone() == None):
                self.errorLabel.setText('Incorrect username or password')
            else:
                # hash password
                password = sha256(password.encode()).hexdigest()

                # check if username and hashed password are in database
                c.execute('SELECT * FROM all_users WHERE username=? AND password=?', (username, password))
                row = c.fetchone()
                if (row == None):
                    self.errorLabel.setText('Incorrect username or password')
                else:
                    # get id of user
                    global id
                    id = row[2]

                    # change the text to green
                    self.errorLabel.setStyleSheet('color: green')
                    self.errorLabel.setText('Login successful')
                    QTimer.singleShot(1000, lambda: self.show_landing_window()) # show landing window after 1 second
            c.close()

    def show_landing_window(self):
        landing_window = LandingWindow()
        stacked_window.addWidget(landing_window)
        stacked_window.setCurrentIndex(2)