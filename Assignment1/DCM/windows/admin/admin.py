from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QTableWidget, QPushButton
from PyQt5.uic import loadUi

from sqlite3 import connect


class AdminWindow(QMainWindow): # admin page
    def __init__(self, stacked_window):
        super(AdminWindow, self).__init__()
        loadUi('./windows/admin/admin.ui', self)
        self.stacked_window = stacked_window
        self.stacked_window.setWindowTitle("Admin")
        self.backButton.clicked.connect(self.back_clicked)
        
        self.load_page()

    def load_page(self): # load data
        self.load_label()
        self.load_table()

    def load_label(self): # load data
        label = self.pageLabel
        label.setText('Admin Page')
        label.move(500, 50)
        label.setFixedWidth(200)
        label.setFixedHeight(50)
        label.setStyleSheet('font: 80 18pt "MS Shell Dlg 2";')

    def load_table(self): # load data
        table = self.adminTable

        conn = connect('./users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM all_users')
        data = c.fetchall()

        # if no data, hide table
        if len(data) == 0:
            self.adminTable.hide()

        table.setRowCount(len(data))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['ID', 'Username', 'Notes', 'Remove'])
        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 750)
        table.setColumnWidth(3, 100)
        table.setFixedWidth(1100)
        table.setFixedHeight(600)
        table.move(50, 150)
        table.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # populate table with patient data
        for i in range(len(data)):
            for j in range(len(data[i])):
                if j == 0: # load username
                    table.setItem(i, 1, QTableWidgetItem(str(data[i][j])))
                elif j == 1: # don't show password
                    continue
                elif j == 2: # load ID
                    table.setItem(i, 0, QTableWidgetItem(str(data[i][j])))

            # create remove button
            removeButton = QPushButton()
            removeButton.setText('Remove')
            removeButton.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')
            removeButton.clicked.connect(self.remove_clicked)
            table.setCellWidget(i, 3, removeButton)

    def remove_clicked(self): # if remove button is clicked, show popup window
        global id
        button = self.sender()
        row = self.adminTable.indexAt(button.pos()).row()
        id = self.adminTable.item(row, 0).text()

        self.show_removepopup()

    def show_removepopup(self): # declare the below popup window
        msg = QMessageBox()
        msg.setWindowTitle('Confirm Remove')
        msg.setText('Are you sure you want to remove this user?')
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        msg.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')

        msg.buttonClicked.connect(self.remove_button)
        x = msg.exec_()

    def remove_button(self, buttonSelected): # if yes is clicked, remove user
        if buttonSelected.text() == '&Yes':
            self.remove_user()
        else:
            pass

    def remove_user(self):
        # remove user from database
        conn = connect('./users.db')
        c = conn.cursor()
        c.execute('DELETE FROM all_users WHERE id = ?', (id,))
        c.execute('DELETE FROM AOO_data WHERE id = ?', (id,))
        c.execute('DELETE FROM VOO_data WHERE id = ?', (id,))
        c.execute('DELETE FROM AAI_data WHERE id = ?', (id,))
        c.execute('DELETE FROM VVI_data WHERE id = ?', (id,))
        c.execute('DELETE FROM AOOR_data WHERE id = ?', (id,))
        c.execute('DELETE FROM VOOR_data WHERE id = ?', (id,))
        c.execute('DELETE FROM AAIR_data WHERE id = ?', (id,))
        c.execute('DELETE FROM VVIR_data WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        # reload page
        self.stacked_window.removeWidget(self.stacked_window.widget(1))
        self.stacked_window.removeWidget(self.stacked_window.widget(1))
        self.stacked_window.addWidget(AdminWindow(self.stacked_window))
        self.stacked_window.setCurrentIndex(1)
    
    def back_clicked(self): # if back button is clicked, show popup window
        self.show_backpopup()

    def show_backpopup(self): # declare the below popup window
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
            self.stacked_window.setWindowTitle("Welcome")
        else:
            pass
        