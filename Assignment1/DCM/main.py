import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QMainWindow, QStackedWidget
from sqlite3 import connect

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('welcome.ui', self)
        self.setWindowTitle('Welcome')
        self.loginButton.clicked.connect(self.login_clicked)
        self.signUpButton.clicked.connect(self.signup_clicked)

    def login_clicked(self):
        login_window = LoginWindow()
        stacked_window.addWidget(login_window)
        stacked_window.setCurrentIndex(1)

    def signup_clicked(self):
        signup_window = SignupWindow()
        stacked_window.addWidget(signup_window)
        stacked_window.setCurrentIndex(1)

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi('login.ui', self)
        self.setWindowTitle('Login')
        self.backButton.clicked.connect(self.back_clicked)
        self.loginConfirm.clicked.connect(self.check_login)

    def back_clicked(self):
        stacked_window.setCurrentIndex(0)
        # clear stacked window
        stacked_window.removeWidget(stacked_window.widget(1))

    def check_login(self):
        username = self.usernameField.text()
        password = self.passwordField.text()
       
        if (len(username) == 0 or len(password) == 0):
            self.errorLabel.setText('Please fill in all fields')
        else:
            # check if username and password are in database
            conn = connect('users.db')
            c = conn.cursor()
            # check if only username is in database
            c.execute('SELECT * FROM all_users WHERE username=?', (username,))
            # if username is not in database, fetchone() will return None
            if (c.fetchone() == None):
                self.errorLabel.setText('Username does not exist.')
            else:
                # check if username and password are in database
                c.execute('SELECT * FROM all_users WHERE username=? AND password=?', (username, password))
                # if username and password are not in database, fetchone() will return None
                if (c.fetchone() == None):
                    self.errorLabel.setText('Incorrect password.')
                else:
                    self.errorLabel.setText('Login successful')



class SignupWindow(QMainWindow):
    def __init__(self):
        super(SignupWindow, self).__init__()
        loadUi('signup.ui', self)
        self.setWindowTitle('Sign Up')
        self.backButton.clicked.connect(self.back_clicked)
        self.signUpConfirm.clicked.connect(self.check_signup)

    def back_clicked(self):
        stacked_window.setCurrentIndex(0)
        # clear stacked window
        stacked_window.removeWidget(stacked_window.widget(1))

    def check_signup(self):
        username = self.usernameField.text()
        password = self.passwordField.text()

        if (len(username) == 0 or len(password) == 0):
            self.errorLabel.setText('Please fill in all fields')

        else:
            # check if username is already in database
            conn = connect('users.db')
            c = conn.cursor()
            c.execute('SELECT * FROM all_users WHERE username=?', (username,))
            # if username is not in database, fetchone() will return None
            if (c.fetchone() == None):
               # check if password and confirm password match
                if (self.passwordField.text() == self.confirmPasswordField.text()):
                    # add username and password to database
                    c.execute('INSERT INTO all_users VALUES (?, ?)', (username, password))
                    conn.commit()
                    self.errorLabel.setText('Sign up successful')
                else:
                    self.errorLabel.setText('Passwords do not match.')
            else:
                self.errorLabel.setText('Username already exists.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    stacked_window = QStackedWidget()
    stacked_window.addWidget(window)
    stacked_window.setFixedWidth(1200)
    stacked_window.setFixedHeight(800)
    stacked_window.show()
    sys.exit(app.exec_())
    
