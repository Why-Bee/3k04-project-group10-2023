from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

from windows.admin.admin import AdminWindow


class AdminLoginWindow(QMainWindow): # admin login page
    def __init__(self):
        super(AdminLoginWindow, self).__init__()
        loadUi('adminLogin.ui', self)
        self.setWindowTitle('Admin Login')
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
            if username == "doctor" and password == "doctor":    
                # change the text to green
                self.errorLabel.setStyleSheet('color: green')
                self.errorLabel.setText('Login successful')
                QTimer.singleShot(1000, lambda: self.show_admin_window()) # show landing window after 1 second
            else:
                self.errorLabel.setText('Incorrect username or password')

    def show_admin_window(self):
        admin_window = AdminWindow()
        stacked_window.addWidget(admin_window)
        stacked_window.setCurrentIndex(2)