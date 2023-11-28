from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

from sqlite3 import connect
from hashlib import sha256

from windows.landingpage.landingpage import LandingWindow



class LoginWindow(QMainWindow):
    def __init__(self, stacked_window):
        super(LoginWindow, self).__init__()
        loadUi('./windows/login/login.ui', self)
        self.stacked_window = stacked_window
        self.stacked_window.setWindowTitle("Login")
        self.backButton.clicked.connect(self.back_clicked)
        self.loginConfirm.clicked.connect(self.check_login)

        # Initialize id variable
        self.id = None


    def back_clicked(self): # if back button is clicked, go back to welcome screen
        self.stacked_window.setCurrentIndex(0)
        # clear stack
        self.stacked_window.removeWidget(self.stacked_window.widget(1))
        self.stacked_window.setWindowTitle("Welcome")

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
                    self.id = row[2]

                    # change the text to green
                    self.errorLabel.setStyleSheet('color: green')
                    self.errorLabel.setText('Login successful')
                    QTimer.singleShot(1000, lambda: self.show_landing_window()) # show landing window after 1 second
            c.close()

    def show_landing_window(self):
        landing_window = LandingWindow(self.stacked_window, self.id)
        self.stacked_window.addWidget(landing_window)
        self.stacked_window.setCurrentIndex(2)
