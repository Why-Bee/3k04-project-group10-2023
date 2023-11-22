from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class AdminWindow(QMainWindow): # admin page
    def __init__(self, stacked_window):
        super(AdminWindow, self).__init__()
        loadUi('./windows/admin/admin.ui', self)
        self.setWindowTitle('Admin')
        self.stacked_window = stacked_window
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
            self.stacked_window.setCurrentIndex(0)
            # clear stack
            self.stacked_window.removeWidget(self.stacked_window.widget(1))
            self.stacked_window.removeWidget(self.stacked_window.widget(1))
        else:
            pass