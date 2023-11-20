from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class AdminWindow(QMainWindow): # admin page
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi('admin.ui', self)
        self.setWindowTitle('Admin')
        self.backButton.clicked.connect(self.back_clicked)

    
    def back_clicked(self): # if back button is clicked, show popup window
        self.show_popup()

    def show_popup(self): # declare the below popup window
        msg = QMessageBox()
        msg.setWindowTitle('Confirm Logout')
        msg.setText('Are you sure you want to logout?')
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        msg.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')

        msg.buttonClicked.connect(self.popup_button)
        x = msg.exec_()

    def popup_button(self, buttonSelected): # if yes is clicked, go back to welcome screen
        if buttonSelected.text() == '&Yes':
            stacked_window.setCurrentIndex(0)
            # clear stack
            stacked_window.removeWidget(stacked_window.widget(1))
            stacked_window.removeWidget(stacked_window.widget(1))
        else:
            pass