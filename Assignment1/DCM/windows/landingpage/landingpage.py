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

        # set default values to initialize variables
        self.current_mode = '' # current mode of device
        self.connectionStatus = False # connected status of device
        self.id = id # id of current user
        self.setUsername() # set username label

        self.setColours() # reset colours of labels

        # here we would interface with the device to get the current state and which mode is enabled
        # possibly cross reference with database to get the current values of the parameters and make sure they match
        self.board_interface()

        self.updateModeLabel() # update mode label
        self.updateParamLabels() # update param labels with values from database

        # connect buttons to functions
        self.backButton.clicked.connect(self.back_clicked)
        self.connection_Button.clicked.connect(self.toggleConnectionStatus)
        self.changemode_Button.clicked.connect(self.changemode_clicked)
        self.lowerLimit_Button.clicked.connect(lambda: self.updateParam('lower_rate_limit'))
        self.upperLimit_Button.clicked.connect(lambda: self.updateParam('upper_rate_limit'))
        self.AAmp_Button.clicked.connect(lambda: self.updateParam('atrial_amplitude'))
        self.APW_Button.clicked.connect(lambda: self.updateParam('atrial_pulse_width'))
        self.VAmp_Button.clicked.connect(lambda: self.updateParam('ventricular_amplitude'))
        self.VPW_Button.clicked.connect(lambda: self.updateParam('ventricular_pulse_width'))
        self.ARP_Button.clicked.connect(lambda: self.updateParam('ARP'))
        self.VRP_Button.clicked.connect(lambda: self.updateParam('VRP'))


    def setUsername(self): # set username label, called when landing window is created
        conn = connect('users.db')
        c = conn.cursor()
        c.execute('SELECT username FROM all_users WHERE id=?', (self.id,))
        username = c.fetchone()[0]
        self.user_Value.setText(username)
        c.close()

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

    def board_interface(self):
        # make UART connection with board
        # send command to board to get current mode
        # send command to board to get current values of parameters
        # for now, pretend board is connected and we start in AOO mode

        # check if board is connected
        connected = True # for now pretend board is connected

        if connected: # if connected, toggle connection status to true -> default is false
            self.toggleConnectionStatus() # update connected status

        self.current_mode = 'AOO' # pretend we start in AOO mode

    def updateModeLabel(self): # update mode label, called when mode is changed
        if self.current_mode == '':
            self.device_mode_Value.setText('N/A (Not Connected)') # if no mode is selected, set label to blank
        else:
            self.device_mode_Value.setText(self.current_mode)

    def updateLabelsBlank(self):
        # if no mode is selected, set all labels to blank
        self.lowerLimit_Value.setText('--')
        self.lowerLimit_Button.hide()
        self.upperLimit_Value.setText('--')
        self.upperLimit_Button.hide()
        self.AAmp_Value.setText('--')
        self.AAmp_Button.hide()
        self.APW_Value.setText('--')
        self.APW_Button.hide()
        self.VAmp_Value.setText('--')
        self.VAmp_Button.hide()
        self.VPW_Value.setText('--')
        self.VPW_Button.hide()
        self.ARP_Value.setText('--')
        self.ARP_Button.hide()
        self.VRP_Value.setText('--')
        self.VRP_Button.hide()

    def updateParamLabels(self): # update param labels with values from database
        mode = self.current_mode
        # dictionary of modes and their parameters
        modes = {'AOO': ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width'), 'VOO': ('lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width'), 'AAI': ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'ARP'), 'VVI': ('lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width', 'VRP'), 'AOOR': ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'activity_threshold', 'reaction_time', 'response_factor', 'recovery_time'), 'VOOR': ('lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width', 'activity_threshold', 'reaction_time', 'response_factor', 'recovery_time'), 'AAIR': ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'ARP', 'activity_threshold', 'reaction_time', 'response_factor', 'recovery_time'), 'VVIR': ('lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width', 'VRP', 'activity_threshold', 'reaction_time', 'response_factor', 'recovery_time')}
        # tuple of all params
        all_params = ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'ventricular_amplitude', 'ventricular_pulse_width', 'ARP', 'VRP')

        conn = connect('users.db')
        c = conn.cursor()
        
        if mode in modes:
            params = modes[mode] # get params for mode

            # go through all params and update labels
            for param in all_params:

                if param in params: # if param is in mode, get value from database and update label
                    c.execute(f'SELECT {param} FROM {mode}_data WHERE id=?', (self.id,))
                    value = c.fetchone()[0]
                    if param == 'ARP' or param == 'VRP':
                        value = value / 1000
                    value = str(value)

                    if param == 'lower_rate_limit':
                        self.lowerLimit_Value.setText(value)
                        self.lowerLimit_Button.show()
                    elif param == 'upper_rate_limit':
                        self.upperLimit_Value.setText(value)
                        self.upperLimit_Button.show()
                    elif param == 'atrial_amplitude':
                        self.AAmp_Value.setText(value)
                        self.AAmp_Button.show()
                    elif param == 'atrial_pulse_width':
                        self.APW_Value.setText(value)
                        self.APW_Button.show()
                    elif param == 'ventricular_amplitude':
                        self.VAmp_Value.setText(value)
                        self.VAmp_Button.show()
                    elif param == 'ventricular_pulse_width':
                        self.VPW_Value.setText(value)
                        self.VPW_Button.show()
                    elif param == 'ARP':
                        self.ARP_Value.setText(value)
                        self.ARP_Button.show()
                    elif param == 'VRP':
                        self.VRP_Value.setText(value)
                        self.VRP_Button.show()

                else: # if param is not in mode, set label to blank and hide button
                    if param == 'lower_rate_limit':
                        self.lowerLimit_Value.setText('--')
                        self.lowerLimit_Button.hide()
                    elif param == 'upper_rate_limit':
                        self.upperLimit_Value.setText('--')
                        self.upperLimit_Button.hide()
                    elif param == 'atrial_amplitude':
                        self.AAmp_Value.setText('--')
                        self.AAmp_Button.hide()
                    elif param == 'atrial_pulse_width':
                        self.APW_Value.setText('--')
                        self.APW_Button.hide()
                    elif param == 'ventricular_amplitude':
                        self.VAmp_Value.setText('--')
                        self.VAmp_Button.hide()
                    elif param == 'ventricular_pulse_width':
                        self.VPW_Value.setText('--')
                        self.VPW_Button.hide()
                    elif param == 'ARP':
                        self.ARP_Value.setText('--')
                        self.ARP_Button.hide()
                    elif param == 'VRP':
                        self.VRP_Value.setText('--')
                        self.VRP_Button.hide()

        else: # if no mode is selected, set all labels to blank
            self.updateLabelsBlank()

        c.close()

    def toggleConnectionStatus(self): # toggle connection status & related labels, called when connection status is changed
        self.connectionStatus = not self.connectionStatus # toggle connection status

        # update all related labels
        if self.connectionStatus: # if connected to device
            self.connectedStatusText.setText('CONNECTED') # display connected message
            self.connectedStatusText.setStyleSheet('color:rgb(0, 170, 0); font: 75 12pt "MS Shell Dlg 2";')
            self.connectedStatusIcon.setPixmap(QPixmap('./assets/connected.png')) # change pixmap of label to connected
            self.connection_Button.setText('Disconnect') # toggle connect / disconnect button
            self.current_mode = 'AOO' # for now, pretend we start in AOO mode
            self.changemode_Button.show() # hide change mode button
            self.updateModeLabel() # update mode label
            self.updateParamLabels() # set all labels to blank

        else: # if not connected to device
            self.connectedStatusText.setText('DISCONNECTED') # display disconnected message
            self.connectedStatusText.setStyleSheet('color: red; font: 75 12pt "MS Shell Dlg 2";')
            self.connectedStatusIcon.setPixmap(QPixmap('./assets/disconnected.png')) # change pixmap of label to disconnected
            self.connection_Button.setText('Connect') # toggle connect / disconnect button
            self.current_mode = '' # set mode to blank
            self.changemode_Button.hide() # show change mode button
            self.updateModeLabel() # update mode label
            self.updateLabelsBlank() # set all labels to blank
            
        
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
            self.updateModeLabel() # update mode label
            self.updateParamLabels() # update param labels with values from database

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

    def updateParam(self, param): # update param label and in database
        # get current value of param from database
        conn = connect('users.db')
        c = conn.cursor()
        c.execute(f'SELECT {param} FROM {self.current_mode}_data WHERE id=?', (self.id,))
        value = c.fetchone()[0]
        c.close()

        # get new value from user
        if param == 'ARP' or param == 'VRP':
            value, done = QInputDialog.getInt(self, 'Update Parameter', f'Enter a new value for {param}', value, 150, 5000, 1)
        else:
            value, done = QInputDialog.getInt(self, 'Update Parameter', f'Enter a new value for {param}', value, 0, 50, 1)

        if done and self.validateInputs(value): # if input is valid, update label and database
            # update label
            if param == 'lower_rate_limit':
                self.lowerLimit_Value.setText(str(value))
            elif param == 'upper_rate_limit':
                self.upperLimit_Value.setText(str(value))
            elif param == 'atrial_amplitude':
                self.AAmp_Value.setText(str(value))
            elif param == 'atrial_pulse_width':
                self.APW_Value.setText(str(value))
            elif param == 'ventricular_amplitude':
                self.VAmp_Value.setText(str(value))
            elif param == 'ventricular_pulse_width':
                self.VPW_Value.setText(str(value))
            elif param == 'ARP':
                self.ARP_Value.setText(str(value))
            elif param == 'VRP':
                self.VRP_Value.setText(str(value))

            # update database
            conn = connect('users.db')
            c = conn.cursor()
            c.execute(f'UPDATE {self.current_mode}_data SET {param}=? WHERE id=?', (value, self.id))
            conn.commit()
            c.close()

        else: # if input is invalid, show error message
            msg = QMessageBox()
            msg.setWindowTitle('Invalid Input')
            msg.setText('Invalid input. Please ensure you enter a valid value.')
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')
            x = msg.exec_()

    def validateInputs (self, params):
        # check if inputs are valid
        # if not, show error message
        # if yes, update values in database
        # return true if inputs are valid, false if not
        return True # for now, pretend inputs are valid
 