from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

from windows.admin.admin import AdminWindow


class AdminLoginWindow(QMainWindow): # admin login page
    def __init__(self, stacked_window):
        super(AdminLoginWindow, self).__init__()
        loadUi('./windows/adminLogin/adminLogin.ui', self)
        self.stacked_window = stacked_window
        self.stacked_window.setWindowTitle("Admin Login")
        self.backButton.clicked.connect(self.back_clicked)
        self.loginConfirm.clicked.connect(self.check_login)


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
            if username == "doctor" and password == "doctor":    
                # change the text to green
                self.errorLabel.setStyleSheet('color: green')
                self.errorLabel.setText('Login successful')
                QTimer.singleShot(1000, lambda: self.show_admin_window()) # show landing window after 1 second
            else:
                self.errorLabel.setText('Incorrect username or password')

    def show_admin_window(self):
        admin_window = AdminWindow(self.stacked_window)
        self.stacked_window.addWidget(admin_window)
        self.stacked_window.setCurrentIndex(2)
        