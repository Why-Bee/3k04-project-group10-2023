import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QMainWindow, QStackedWidget

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

    def back_clicked(self):
        stacked_window.setCurrentIndex(0)
        # clear stacked window
        stacked_window.removeWidget(stacked_window.widget(1))

class SignupWindow(QMainWindow):
    def __init__(self):
        super(SignupWindow, self).__init__()
        loadUi('signup.ui', self)
        self.setWindowTitle('Sign Up')
        self.backButton.clicked.connect(self.back_clicked)

    def back_clicked(self):
        stacked_window.setCurrentIndex(0)
        # clear stacked window
        stacked_window.removeWidget(stacked_window.widget(1))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    stacked_window = QStackedWidget()
    stacked_window.addWidget(window)
    stacked_window.setFixedWidth(1200)
    stacked_window.setFixedHeight(800)
    stacked_window.show()
    sys.exit(app.exec_())
    
