from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from windows.login.login import LoginWindow
from windows.signup.signup import SignupWindow
from windows.adminLogin.adminLogin import AdminLoginWindow


class MyWindow(QMainWindow): # Welcome screen 
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('./windows/welcome/welcome.ui', self) 
        self.setWindowTitle('Welcome')
        self.adminButton.clicked.connect(self.admin_clicked)
        self.loginButton.clicked.connect(self.login_clicked) 
        self.signUpButton.clicked.connect(self.signup_clicked)

    
    def admin_clicked(self): # if admin button is clicked, show admin window
        adminLogin_window = AdminLoginWindow()
        stacked_window.addWidget(adminLogin_window)
        stacked_window.setCurrentIndex(1)

    def login_clicked(self): # if login button is clicked, show login window
        login_window = LoginWindow()
        stacked_window.addWidget(login_window)
        stacked_window.setCurrentIndex(1)

    def signup_clicked(self): # if signup button is clicked, show signup window
        signup_window = SignupWindow()
        stacked_window.addWidget(signup_window)
        stacked_window.setCurrentIndex(1)