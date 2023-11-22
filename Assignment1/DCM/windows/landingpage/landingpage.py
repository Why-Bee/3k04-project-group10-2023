from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

from sqlite3 import connect


pConnect = False # if connected to device, will be True. implement later


class LandingWindow(QMainWindow): # landing page
    def __init__(self, stacked_window):
        super(LandingWindow, self).__init__()
        loadUi('./windows/landingpage/landingpage.ui', self)
        self.setWindowTitle('Landing Page')
        self.stacked_window = stacked_window

        # self.updateLabels() # update labels with values from database

        self.backButton.clicked.connect(self.back_clicked)
        self.editAOO_Button.clicked.connect(self.editAOO_clicked)
        self.editVOO_Button.clicked.connect(self.editVOO_clicked)
        self.editAAI_Button.clicked.connect(self.editAAI_clicked)
        self.editVVI_Button.clicked.connect(self.editVVI_clicked)


        if not pConnect: # if not connected to device, display disconnected message
            self.connectedStatusText.setText('DISCONNECTED')
            self.connectedStatusText.setStyleSheet('color: red; font: 75 12pt "MS Shell Dlg 2";')
            # change pixmap of label to disconnected
            self.connectedStatusIcon.setPixmap(QPixmap('./assets/disconnected.png'))

        else: # if connected to device, display connected message
            self.connectedStatusText.setText('CONNECTED')
            self.connectedStatusText.setStyleSheet('color:rgb(0, 170, 0); font: 75 12pt "MS Shell Dlg 2";')
            # change pixmap of label to connected
            self.connectedStatusIcon.setPixmap(QPixmap('./assets/connected.png'))
        
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

    def updateLabels(self): # update labels with values from database
        conn = connect('users.db')
        c = conn.cursor()
        # fetch username
        c.execute('SELECT * FROM all_users WHERE id=?', (id,))
        username = c.fetchone()[0]
        self.user_Value.setText(username)
        c.execute('SELECT * FROM lower_rate_limit WHERE id=?', (id,))
        ll = c.fetchone()[1]
        self.lowerLimit_Value.setText(str(ll))
        c.execute('SELECT * FROM upper_rate_limit WHERE id=?', (id,))
        ul = c.fetchone()[1]
        self.upperLimit_Value.setText(str(ul))
        c.execute('SELECT * FROM atrial_amplitude WHERE id=?', (id,))
        aa = c.fetchone()[1]
        self.AAmp_Value.setText(str(aa/10))
        c.execute('SELECT * FROM atrial_pulse_width WHERE id=?', (id,))
        apw = c.fetchone()[1]
        self.APW_Value.setText(str(apw/10))
        c.execute('SELECT * FROM ventricular_amplitude WHERE id=?', (id,))
        va = c.fetchone()[1]
        self.VAmp_Value.setText(str(va/10))
        c.execute('SELECT * FROM ventricular_pulse_width WHERE id=?', (id,))
        vpw = c.fetchone()[1]
        self.VPW_Value.setText(str(vpw/10))
        c.execute('SELECT * FROM ARP WHERE id=?', (id,))
        arp = c.fetchone()[1]
        self.ARP_Value.setText(str(arp))
        c.execute('SELECT * FROM VRP WHERE id=?', (id,))
        vrp = c.fetchone()[1]
        self.VRP_Value.setText(str(vrp))
        c.close()

    def editAOO_clicked(self):
        # use input dialog to get new values
        ll, done1 = QInputDialog.getInt(self, 'Lower Rate Limit', 'Enter a new value for lower rate limit')
        ul, done2 = QInputDialog.getInt(self, 'Upper Rate Limit', 'Enter a new value for upper rate limit')
        aa, done3 = QInputDialog.getDouble(self, 'Atrial Amplitude', 'Enter a new value for atrial amplitude')
        apw, done4 = QInputDialog.getDouble(self, 'Atrial Pulse Width', 'Enter a new value for atrial pulse width')

        if done1 and done2 and done3 and done4: # if all inputs are valid
            # update values in database
            

            if validateInputs(ll, ul, aa, apw):
                conn = connect('users.db')
                c = conn.cursor()
                c.execute('UPDATE lower_rate_limit SET value=? WHERE id=?', (ll, id))
                c.execute('UPDATE upper_rate_limit SET value=? WHERE id=?', (ul, id))
                c.execute('UPDATE atrial_amplitude SET value=? WHERE id=?', (int(aa*10), id))
                c.execute('UPDATE atrial_pulse_width SET value=? WHERE id=?', (int(apw*10), id))
                conn.commit()
                c.close()
                # update values in landing window
                self.lowerLimit_Value.setText(str(ll))
                self.upperLimit_Value.setText(str(ul))
                self.AAmp_Value.setText(str(aa))
                self.APW_Value.setText(str(apw))
            else:
                # if inputs are invalid, show error message
                msg = QMessageBox()
                msg.setWindowTitle('Invalid Inputs')
                msg.setText('Inputs are invalid. Please try again. Your changes have not been saved.')
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)
                msg.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')
                x = msg.exec_()
            c.close()
   

    def editVOO_clicked(self):
        # use input dialog to get new values
        ll, done1 = QInputDialog.getInt(self, 'Lower Rate Limit', 'Enter a new value for lower rate limit')
        ul, done2 = QInputDialog.getInt(self, 'Upper Rate Limit', 'Enter a new value for upper rate limit')
        va, done3 = QInputDialog.getDouble(self, 'Ventricular Amplitude', 'Enter a new value for ventricular amplitude')
        vpw, done4 = QInputDialog.getDouble(self, 'Ventricular Pulse Width', 'Enter a new value for ventricular pulse width')

        if done1 and done2 and done3 and done4:
            # update values in database
            if validateInputs(ll, ul, va, vpw):
                conn = connect('users.db')
                c = conn.cursor()
                c.execute('UPDATE lower_rate_limit SET value=? WHERE id=?', (ll, id))
                c.execute('UPDATE upper_rate_limit SET value=? WHERE id=?', (ul, id))
                c.execute('UPDATE ventricular_amplitude SET value=? WHERE id=?', (int(va*10), id))
                c.execute('UPDATE ventricular_pulse_width SET value=? WHERE id=?', (int(vpw*10), id))
                conn.commit()
                c.close()

                # update values in landing window
                self.lowerLimit_Value.setText(str(ll))
                self.upperLimit_Value.setText(str(ul))
                self.VAmp_Value.setText(str(va))
                self.VPW_Value.setText(str(vpw))
            else:
                # if inputs are invalid, show error message
                msg = QMessageBox()
                msg.setWindowTitle('Invalid Inputs')
                msg.setText('Inputs are invalid. Please try again. Your changes have not been saved.')
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)
                msg.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')
                x = msg.exec_()

    def editAAI_clicked(self):
        # use input dialog to get new values
        ll, done1 = QInputDialog.getInt(self, 'Lower Rate Limit', 'Enter a new value for lower rate limit')
        ul, done2 = QInputDialog.getInt(self, 'Upper Rate Limit', 'Enter a new value for upper rate limit')
        aa, done3 = QInputDialog.getDouble(self, 'Atrial Amplitude', 'Enter a new value for atrial amplitude')
        apw, done4 = QInputDialog.getDouble(self, 'Atrial Pulse Width', 'Enter a new value for atrial pulse width')
        arp, done5 = QInputDialog.getInt(self, 'ARP', 'Enter a new value for ARP')

        if done1 and done2 and done3 and done4 and done5:
            # update values in database
            conn = connect('users.db')
            c = conn.cursor()
            c.execute('UPDATE lower_rate_limit SET value=? WHERE id=?', (ll, id))
            c.execute('UPDATE upper_rate_limit SET value=? WHERE id=?', (ul, id))
            c.execute('UPDATE atrial_amplitude SET value=? WHERE id=?', (int(aa*10), id))
            c.execute('UPDATE atrial_pulse_width SET value=? WHERE id=?', (int(apw*10), id))
            c.execute('UPDATE ARP SET value=? WHERE id=?', (arp, id))
            conn.commit()
            c.close()

            # update values in landing window
            self.lowerLimit_Value.setText(str(ll))
            self.upperLimit_Value.setText(str(ul))
            self.AAmp_Value.setText(str(aa))
            self.APW_Value.setText(str(apw))
            self.ARP_Value.setText(str(arp))

    def editVVI_clicked(self):
        # use input dialog to get new values
        ll, done1 = QInputDialog.getInt(self, 'Lower Rate Limit', 'Enter a new value for lower rate limit')
        ul, done2 = QInputDialog.getInt(self, 'Upper Rate Limit', 'Enter a new value for upper rate limit')
        va, done3 = QInputDialog.getDouble(self, 'Ventricular Amplitude', 'Enter a new value for ventricular amplitude')
        vpw, done4 = QInputDialog.getDouble(self, 'Ventricular Pulse Width', 'Enter a new value for ventricular pulse width')
        vrp, done5 = QInputDialog.getInt(self, 'VRP', 'Enter a new value for VRP')

        if done1 and done2 and done3 and done4 and done5:
            # update values in database
            conn = connect('users.db')
            c = conn.cursor()
            c.execute('UPDATE lower_rate_limit SET value=? WHERE id=?', (ll, id))
            c.execute('UPDATE upper_rate_limit SET value=? WHERE id=?', (ul, id))
            c.execute('UPDATE ventricular_amplitude SET value=? WHERE id=?', (int(va*10), id))
            c.execute('UPDATE ventricular_pulse_width SET value=? WHERE id=?', (int(vpw*10), id))
            c.execute('UPDATE VRP SET value=? WHERE id=?', (vrp, id))
            conn.commit()
            c.close()

            # update values in landing window
            self.lowerLimit_Value.setText(str(ll))
            self.upperLimit_Value.setText(str(ul))
            self.VAmp_Value.setText(str(va))
            self.VPW_Value.setText(str(vpw))
            self.VRP_Value.setText(str(vrp))