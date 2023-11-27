from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

from sqlite3 import connect


class LandingWindow(QMainWindow): # landing page
    def __init__(self, stacked_window, id):
        super(LandingWindow, self).__init__()
        loadUi('./windows/landingpage/landingpage.ui', self)
        self.stacked_window = stacked_window
        self.stacked_window.setWindowTitle("Landing Page")

        self.id = id # id of current user
        self.setUsername() # set username label

        # set default values to initialize variables
        self.current_mode = '' # current mode of device
        self.pConnect = False # connected status of device

        self.setColours() # reset colours of labels

        # here we would interface with the device to get the current state and which mode is enabled
        # possibly cross reference with database to get the current values of the parameters and make sure they match
        self.board_interface()

        self.updateMode() # update mode label
        self.updateLabels() # update param labels with values from database

        # connect buttons to functions
        self.backButton.clicked.connect(self.back_clicked)
        self.changemode_Button.clicked.connect(self.changemode_clicked)
        self.editAOO_Button.clicked.connect(self.editAOO_clicked)
        self.editVOO_Button.clicked.connect(self.editVOO_clicked)
        self.editAAI_Button.clicked.connect(self.editAAI_clicked)
        self.editVVI_Button.clicked.connect(self.editVVI_clicked)
        self.editAOOR_Button.clicked.connect(self.editAOOR_clicked)
        self.editVOOR_Button.clicked.connect(self.editVOOR_clicked)
        self.editAAIR_Button.clicked.connect(self.editAAIR_clicked)
        self.editVVIR_Button.clicked.connect(self.editVVIR_clicked)


    def board_interface(self):
        # make UART connection with board
        # send command to board to get current mode
        # send command to board to get current values of parameters
        # for now, pretend board is connected and we start in AOO mode

        # check if board is connected
        connected = True # for now pretend board is connected

        if connected:
            self.pConnect = True # change connected status to true
            self.updatecPConnect() # update connected status

        self.current_mode = 'AOO' # pretend we start in AOO mode

    def updateMode(self): # update mode label, called when mode is changed
        self.device_mode_Value.setText(self.current_mode)

    def setUsername(self): # set username label, called when landing window is created
        conn = connect('users.db')
        c = conn.cursor()
        c.execute('SELECT username FROM all_users WHERE id=?', (self.id,))
        username = c.fetchone()[0]
        self.user_Value.setText(username)
        c.close()

    def updatecPConnect(self): # update connected status, called when connected status is changed
        if not self.pConnect: # if not connected to device, display disconnected message
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
            self.stacked_window.setWindowTitle("Welcome")
        else:
            pass

    def changemode_clicked(self): # if change mode button is clicked, show popup window
        modes = ['AOO', 'VOO', 'AAI', 'VVI', 'AOOR', 'VOOR', 'AAIR', 'VVIR']
        mode, done1 = QInputDialog.getItem(self, 'Change Mode', 'Select a new mode', modes)

        if done1 and mode in modes: # Once a mode is selected, if valid, update the mode
            self.current_mode = mode
            self.updateMode() # update mode label
            self.updateLabels() # update param labels with values from database
        else:
            # if input is invalid, show error message
            msg = QMessageBox()
            msg.setWindowTitle('Invalid Input')
            msg.setText('Invalid input. Please ensure you select a valid mode.')
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')
            x = msg.exec_()

    def updateLabels(self): # update labels with values from database
        mode = self.current_mode
        conn = connect('users.db')
        c = conn.cursor()
        
        # cases for each mode
        if mode == 'AOO':
            self.updateLabelsAOO(c)
        elif mode == 'VOO':
            self.updateLabelsVOO(c)
        elif mode == 'AAI':
            self.updateLabelsAAI(c)
        elif mode == 'VVI':
            self.updateLabelsVVI(c)
        elif mode == 'AOOR':
            self.updateLabelsAOOR(c)
        elif mode == 'VOOR':
            self.updateLabelsVOOR(c)
        elif mode == 'AAIR':
            self.updateLabelsAAIR(c)
        elif mode == 'VVIR':
            self.updateLabelsVVIR(c)
        else:
            self.updateLabelsBlank()

    def setColours(self): # reset colours of labels
        # set all labels to black, no bold, 8pt
        self.lowerLimit_Value.setStyleSheet('color:black; font: 8pt "MS Shell Dlg 2";')
        self.upperLimit_Value.setStyleSheet('color:black; font: 8pt "MS Shell Dlg 2";')
        self.AAmp_Value.setStyleSheet('color:black; font: 8pt "MS Shell Dlg 2";')
        self.APW_Value.setStyleSheet('color:black; font: 8pt "MS Shell Dlg 2";')
        self.VAmp_Value.setStyleSheet('color:black; font: 8pt "MS Shell Dlg 2";')
        self.VPW_Value.setStyleSheet('color:black; font: 8pt "MS Shell Dlg 2";')
        self.ARP_Value.setStyleSheet('color:black; font: 8pt "MS Shell Dlg 2";')
        self.VRP_Value.setStyleSheet('color:black; font: 8pt "MS Shell Dlg 2";')


    def editAOO_clicked(self):
        id = self.id
        # use input dialog to get new values
        ll, done1 = QInputDialog.getInt(self, 'Lower Rate Limit', 'Enter a new value for lower rate limit')
        ul, done2 = QInputDialog.getInt(self, 'Upper Rate Limit', 'Enter a new value for upper rate limit')
        aa, done3 = QInputDialog.getDouble(self, 'Atrial Amplitude', 'Enter a new value for atrial amplitude')
        apw, done4 = QInputDialog.getDouble(self, 'Atrial Pulse Width', 'Enter a new value for atrial pulse width')

        if done1 and done2 and done3 and done4: # if all inputs are valid
            # update values in database
            

            if self.validateInputs([ll, ul, aa, apw]):
                conn = connect('users.db')
                c = conn.cursor()
                c.execute('UPDATE AOO_data SET lower_rate_limit=? WHERE id=?', (ll, id))
                c.execute('UPDATE AOO_data SET upper_rate_limit=? WHERE id=?', (ul, id))
                c.execute('UPDATE AOO_data SET atrial_amplitude=? WHERE id=?', (int(aa*10), id))
                c.execute('UPDATE AOO_data SET atrial_pulse_width=? WHERE id=?', (int(apw*10), id))
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
        id = self.id
        # use input dialog to get new values
        ll, done1 = QInputDialog.getInt(self, 'Lower Rate Limit', 'Enter a new value for lower rate limit')
        ul, done2 = QInputDialog.getInt(self, 'Upper Rate Limit', 'Enter a new value for upper rate limit')
        va, done3 = QInputDialog.getDouble(self, 'Ventricular Amplitude', 'Enter a new value for ventricular amplitude')
        vpw, done4 = QInputDialog.getDouble(self, 'Ventricular Pulse Width', 'Enter a new value for ventricular pulse width')

        if done1 and done2 and done3 and done4:
            # update values in database
            if self.validateInputs([ll, ul, va, vpw]):
                conn = connect('users.db')
                c = conn.cursor()
                c.execute('UPDATE VOO_data SET lower_rate_limit=? WHERE id=?', (ll, id))
                c.execute('UPDATE VOO_data SET upper_rate_limit=? WHERE id=?', (ul, id))
                c.execute('UPDATE VOO_data SET ventricular_amplitude=? WHERE id=?', (int(va*10), id))
                c.execute('UPDATE VOO_data SET ventricular_pulse_width=? WHERE id=?', (int(vpw*10), id))
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
        id = self.id
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
            c.execute('UPDATE AAI_data SET lower_rate_limit=? WHERE id=?', (ll, id))
            c.execute('UPDATE AAI_data SET upper_rate_limit=? WHERE id=?', (ul, id))
            c.execute('UPDATE AAI_data SET atrial_amplitude=? WHERE id=?', (int(aa*10), id))
            c.execute('UPDATE AAI_data SET atrial_pulse_width=? WHERE id=?', (int(apw*10), id))
            c.execute('UPDATE AAI_data SET ARP=? WHERE id=?', (arp, id))
            conn.commit()
            c.close()

            # update values in landing window
            self.lowerLimit_Value.setText(str(ll))
            self.upperLimit_Value.setText(str(ul))
            self.AAmp_Value.setText(str(aa))
            self.APW_Value.setText(str(apw))
            self.ARP_Value.setText(str(arp))

    def editVVI_clicked(self):
        id = self.id
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
            c.execute('UPDATE VVI_data SET lower_rate_limit=? WHERE id=?', (ll, id))
            c.execute('UPDATE VVI_data SET upper_rate_limit=? WHERE id=?', (ul, id))
            c.execute('UPDATE VVI_data SET ventricular_amplitude=? WHERE id=?', (int(va*10), id))
            c.execute('UPDATE VVI_data SET ventricular_pulse_width=? WHERE id=?', (int(vpw*10), id))
            c.execute('UPDATE VVI_data SET VRP=? WHERE id=?', (vrp, id))
            conn.commit()
            c.close()

            # update values in landing window
            self.lowerLimit_Value.setText(str(ll))
            self.upperLimit_Value.setText(str(ul))
            self.VAmp_Value.setText(str(va))
            self.VPW_Value.setText(str(vpw))
            self.VRP_Value.setText(str(vrp))

    def validateInputs (self, params):
        # check if inputs are valid
        # if not, show error message
        # if yes, update values in database
        # return true if inputs are valid, false if not
        return True # for now, pretend inputs are valid
    
    def editAOOR_clicked(self):
        print('edit AOOR clicked')

    def editVOOR_clicked(self):
        print('edit VOOR clicked')

    def editAAIR_clicked(self):
        print('edit AAIR clicked')

    def editVVIR_clicked(self):
        print('edit VVIR clicked')

    def updateLabelsAOO(self, c):
        # update labels with values from database
        id = self.id
        AOO_params = ['lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width']

        for i in range(len(AOO_params)):
            c.execute(f'SELECT {AOO_params[i]} FROM {self.current_mode}_data WHERE id=?', (id,))
            value = c.fetchone()[0]

            if i == 0:
                self.lowerLimit_Value.setText(str(value))
            elif i == 1:
                self.upperLimit_Value.setText(str(value))
            elif i == 2:
                self.AAmp_Value.setText(str(value/10))
            elif i == 3:
                self.APW_Value.setText(str(value/10))

    def updateLabelsVOO(self, c):
        # update labels with values from database
        id = self.id
        VOO_params = ['lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width']

        for i in range(len(VOO_params)):
            c.execute(f'SELECT {VOO_params[i]} FROM {self.current_mode}_data WHERE id=?', (id,))
            value = c.fetchone()[0]

            if i == 0:
                self.lowerLimit_Value.setText(str(value))
            elif i == 1:
                self.upperLimit_Value.setText(str(value))
            elif i == 2:
                self.VAmp_Value.setText(str(value/10))
            elif i == 3:
                self.VPW_Value.setText(str(value/10))

    def updateLabelsAAI(self, c):
        # update labels with values from database
        id = self.id
        AAI_params = ['lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'ARP']

        for i in range(len(AAI_params)):
            c.execute(f'SELECT {AAI_params[i]} FROM {self.current_mode}_data WHERE id=?', (id,))
            value = c.fetchone()[0]

            if i == 0:
                self.lowerLimit_Value.setText(str(value))
            elif i == 1:
                self.upperLimit_Value.setText(str(value))
            elif i == 2:
                self.AAmp_Value.setText(str(value/10))
            elif i == 3:
                self.APW_Value.setText(str(value/10))
            elif i == 4:
                self.ARP_Value.setText(str(value))

    def updateLabelsVVI(self, c):
        # update labels with values from database
        id = self.id
        VVI_params = ['lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width', 'VRP']

        for i in range(len(VVI_params)):
            c.execute(f'SELECT {VVI_params[i]} FROM {self.current_mode}_data WHERE id=?', (id,))
            value = c.fetchone()[0]

            if i == 0:
                self.lowerLimit_Value.setText(str(value))
            elif i == 1:
                self.upperLimit_Value.setText(str(value))
            elif i == 2:
                self.VAmp_Value.setText(str(value/10))
            elif i == 3:
                self.VPW_Value.setText(str(value/10))
            elif i == 4:
                self.VRP_Value.setText(str(value))

    def updateLabelsAOOR(self, c):
        print('updating AOOR labels')

    def updateLabelsVOOR(self, c):
        print('updating VOOR labels')

    def updateLabelsAAIR(self, c):
        print('updating AAIR labels')

    def updateLabelsVVIR(self, c):
        print('updating VVIR labels')

    def updateLabelsBlank(self):
        # if no mode is selected, set all labels to blank
        self.lowerLimit_Value.setText('')
        self.upperLimit_Value.setText('')
        self.AAmp_Value.setText('')
        self.APW_Value.setText('')
        self.VAmp_Value.setText('')
        self.VPW_Value.setText('')
        self.ARP_Value.setText('')
        self.VRP_Value.setText('')
 