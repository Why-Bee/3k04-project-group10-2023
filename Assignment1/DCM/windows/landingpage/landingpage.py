from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

from sqlite3 import connect
# import serial
import struct
import time

# const tuple of all params
ALL_PARAMS = ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'ventricular_amplitude', 'ventricular_pulse_width', 'ARP', 'VRP', 'atrial_sensitivity', 'PVARP', 'hysteresis', 'ventricular_sensitivity', 'max_sensor_rate')


class LandingWindow(QMainWindow): # landing page
    def __init__(self, stacked_window, id):
        super(LandingWindow, self).__init__()
        loadUi('./windows/landingpage/landingpage.ui', self)
        self.stacked_window = stacked_window
        self.stacked_window.setWindowTitle("Landing Page")

        # set default values & initialize variables
        self.current_mode = '' # current mode of device
        self.connectionStatus = False # connected status of device
        self.id = id # id of current user
        self.changemode_Button.hide() # hide change mode button
        self.setUsername() # set username label
        self.setColours() # reset colours of labels

        # here we would interface with the device to get the current state and which mode is enabled
        # possibly cross reference with database to get the current values of the parameters and make sure they match
        self.board_interface()

        self.updateModeLabel() # update mode label
        self.updateParamLabels() # update param labels with values from database

        # connect buttons to functions
        self.back_Button.clicked.connect(self.back_clicked)
        self.connection_Button.clicked.connect(self.connectionButton_clicked)
        self.changemode_Button.clicked.connect(self.changemode_clicked)
        for param in ALL_PARAMS: # connect all param buttons to updateParam function
            button_name = f'{param}_Button'
            getattr(self, button_name).clicked.connect(lambda _, param=param: self.updateParam(param))


    def setUsername(self): # set username label, called when landing window is created
        conn = connect('users.db')
        c = conn.cursor()
        c.execute('SELECT username FROM all_users WHERE id=?', (self.id,))
        username = c.fetchone()[0]
        self.user_Value.setText(username)
        c.close()

    def setColours(self): # reset colours of labels, called when landing window is created
        # set all labels to black, no bold, 8pt
        for param in ALL_PARAMS:
            value_name = f'{param}_Value'
            getattr(self, value_name).setStyleSheet('color: black; font: 8pt "MS Shell Dlg 2";')

    def board_interface(self): # interface with board to get current state and which mode is enabled
        pass
        # # make UART connection with board
        # # send command to board to get current mode
        # # send command to board to get current values of parameters
        # # for now, pretend board is connected and we start in AOO mode

        # # create serial connection
        # try:
        #     ser = serial.Serial('COM7')
        #     connected = ser.is_open
        #     ser.baudrate = 115200
        #     ser.bytesize = 8
        #     ser.parity = 'N'
        #     ser.stopbits = 1

        #     for i in range(1000):
        #         data = struct.pack("B B B B 2B 2B 2B B B B B B B B B 2B 2B 2B", 
        #                     0x16,
        #                     0x16, # echo
        #                     0x01, 
        #                     0x03, 
        #                     0x40, 0x01, 
        #                     0xAC, 0x0D,
        #                     0x90, 0x01,
        #                     0x00,
        #                     0x1E,
        #                     0x78,
        #                     0x5A,
        #                     0x3C,
        #                     0x05,
        #                     0x08,
        #                     0x78,
        #                     0xAC, 0x0D, 
        #                     0x90, 0x01,
        #                     0xFA, 0x00
        #                     )
        #         ser.write(data)
        #         output = ser.read(size=24)
        #         print(output.hex())
        #         time.sleep(0.1)

        #     unpacked = struct.unpack("B B B B 2B 2B 2B B B B B B B B B 2B 2B 2B", output)
        #     temp = unpacked[2]
        #     if temp == 0:
        #         self.current_mode = 'Off'
        #     elif temp == 1:
        #         self.current_mode = 'AOO'
        #     elif temp == 2:
        #         self.current_mode = 'VOO'
        #     elif temp == 3:
        #         self.current_mode = 'AAI'
        #     elif temp == 4:
        #         self.current_mode = 'VVI'

        #     ser.close()

        #     # update mode label
        #     self.updateModeLabel()
            
        # except serial.SerialException:
        #     self.current_mode = 'Off'

        # if connected: # if connected, toggle connection status to true -> default is false
        #     self.toggleConnectionStatus() # update connected status

    # def updateBoard(self, param, value): # update the board with new parameter value
    #     # send command to board to update parameter
    #     # check which parameter is being updated

    #     # create serial connection
    #     try:
    #         ser = serial.Serial('COM7')
    #         connected = ser.is_open
    #         ser.baudrate = 115200
    #         ser.bytesize = 8
    #         ser.parity = 'N'
    #         ser.stopbits = 1

    #         # fetch current values of all parameters
    #         # connect to database
    #         conn = connect('users.db')
    #         c = conn.cursor()
    #         c.execute(f'SELECT * FROM {self.current_mode}_data WHERE id=?', (self.id,))
            
    def updateModeLabel(self): # update mode label, called when mode is changed
        if self.current_mode == '':
            self.device_mode_Value.setText('N/A (Not Connected)') # if no mode is selected, set label to blank
        else:
            self.device_mode_Value.setText(self.current_mode)

    def hideAllParams(self): # hide all param labels & buttons, called when no mode is selected or when device is disconnected
        for param in ALL_PARAMS:
            label_name = f'{param}'
            value_name = f'{param}_Value'
            button_name = f'{param}_Button'
            getattr(self, label_name).hide()
            getattr(self, value_name).hide()
            getattr(self, button_name).hide()

        self.noParams_Label.show()

    def updateParamLabels(self): # update all param labels & buttons to match current mode, called when mode is changed
        mode = self.current_mode
        # dictionary of modes and their parameters
        modes = {'AOO': ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width'), 'VOO': ('lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width'), 'AAI': ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'ARP', 'atrial_sensitivity', 'PVARP', 'hysteresis'), 'VVI': ('lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width', 'VRP', 'hysteresis', 'ventricular_sensitivity'), 'AOOR': ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'activity_threshold', 'reaction_time', 'response_factor', 'recovery_time', 'max_sensor_rate'), 'VOOR': ('lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width', 'activity_threshold', 'reaction_time', 'response_factor', 'recovery_time', 'max_sensor_rate'), 'AAIR': ('lower_rate_limit', 'upper_rate_limit', 'atrial_amplitude', 'atrial_pulse_width', 'ARP', 'atrial_sensitivity', 'activity_threshold', 'reaction_time', 'response_factor', 'recovery_time', 'PVARP', 'hysteresis', 'max_sensor_rate'), 'VVIR': ('lower_rate_limit', 'upper_rate_limit', 'ventricular_amplitude', 'ventricular_pulse_width', 'VRP', 'activity_threshold', 'reaction_time', 'response_factor', 'recovery_time', 'hysteresis', 'ventricular_sensitivity', 'max_sensor_rate')}

        conn = connect('users.db')
        c = conn.cursor()
        
        # check to make sure mode != '' or 'Off', i.e. a mode is selected
        if mode in modes:
            params = modes[mode] # get params for mode

            labelsShown = 0 # keep track of how many labels are shown

            # go through all params and update labels
            for param in ALL_PARAMS:
                label_name = f'{param}'
                value_name = f'{param}_Value'
                button_name = f'{param}_Button'

                if param in params: # if param is in mode, get value from database, update label & show button
                    c.execute(f'SELECT {param} FROM {mode}_data WHERE id=?', (self.id,))
                    value = c.fetchone()[0]
                    if param == 'ARP' or param == 'VRP':
                        value = value / 1000
                    value = str(value)

                    getattr(self, label_name).setGeometry(getattr(self, label_name).x(), 210 + (labelsShown * 40), getattr(self, label_name).width(), 30)
                    getattr(self, label_name).show()

                    getattr(self, value_name).setGeometry(990, 210 + (labelsShown * 40), getattr(self, value_name).width(), 30)
                    getattr(self, value_name).setText(value)
                    getattr(self, value_name).show()

                    getattr(self, button_name).setGeometry(1050, 210 + (labelsShown * 40), 100, 30)
                    getattr(self, button_name).show()
                    labelsShown += 1

                    self.noParams_Label.hide()

                else: # if param is not in mode, set label to blank & hide button
                    getattr(self, label_name).hide()
                    getattr(self, value_name).hide()
                    getattr(self, button_name).hide()

        else: # if no mode is selected, set all labels to blank & hide all buttons
            self.hideAllParams()

        c.close()

    def toggleConnectionStatus(self): # toggle connection status & related labels, called when connection status is changed
        self.connectionStatus = not self.connectionStatus # toggle connection status

        # update all related labels
        if self.connectionStatus: # if connected to device
            self.connectedStatusText.setText('CONNECTED') # display connected message
            self.connectedStatusText.setStyleSheet('color:rgb(0, 170, 0); font: 75 12pt "MS Shell Dlg 2";')
            self.connectedStatusIcon.setPixmap(QPixmap('./assets/connected.png')) # change pixmap of label to connected
            self.connection_Button.setText('Disconnect') # toggle connect / disconnect button
            self.current_mode = 'Off' # for now, pretend we start in Off mode
            self.changemode_Button.show() # hide change mode button
            self.updateModeLabel() # update mode label
            self.updateParamLabels() # update param labels with values from database

        else: # if not connected to device
            self.connectedStatusText.setText('DISCONNECTED') # display disconnected message
            self.connectedStatusText.setStyleSheet('color: red; font: 75 12pt "MS Shell Dlg 2";')
            self.connectedStatusIcon.setPixmap(QPixmap('./assets/disconnected.png')) # change pixmap of label to disconnected
            self.connection_Button.setText('Connect') # toggle connect / disconnect button
            self.current_mode = '' # set mode to blank
            self.changemode_Button.hide() # show change mode button
            self.updateModeLabel() # update mode label
            self.hideAllParams() # set all labels to blank
            
        
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

    def connectionButton_clicked(self):
        if self.connectionStatus:
            # ATTEMPT TO DISCONNECT FROM DEVICE
            # if successful, toggle connection status
            self.toggleConnectionStatus() # for now pretend we disconnect successfully
        else:
            # ATTEMPT TO CONNECT TO DEVICE
            # board_interface(self) # attempt to connect to device
            # if successful, toggle connection status
            self.toggleConnectionStatus() # for now pretend we connect successfully

    def changemode_clicked(self): # if change mode button is clicked, show popup window
        modes = ['Off', 'AOO', 'VOO', 'AAI', 'VVI', 'AOOR', 'VOOR', 'AAIR', 'VVIR']
        mode, done1 = QInputDialog.getItem(self, 'Change Mode', 'Select a new mode', modes)

        if done1 and mode in modes: # Once a mode is selected, if valid, update the mode
            self.current_mode = mode
            self.updateModeLabel() # update mode label
            self.updateParamLabels() # update param labels with values from database

        else: # if input is invalid, show error message
            msg = QMessageBox()
            msg.setWindowTitle('Invalid Input')
            msg.setText('Invalid input. Please ensure you select a valid mode.')
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.setStyleSheet('font: 70 11pt "MS Shell Dlg 2";')
            x = msg.exec_()

    def updateParam(self, param): # update singular param label & database value, called when singe param changed
        # get current value of param from database
        conn = connect('users.db')
        c = conn.cursor()
        c.execute(f'SELECT {param} FROM {self.current_mode}_data WHERE id=?', (self.id,))
        value = c.fetchone()[0]
        c.close()

        # get new value from user
        if param == 'hysteresis':
            value = not value # toggle value
            done = True
        else:
            value, done = QInputDialog.getInt(self, 'Update Parameter', f'Enter a new value for {param}', value)

        if done and self.validateInputs([(param, value)]): # if input is valid, update label and database

            # update label
            value_name = f'{param}_Value'
            getattr(self, value_name).setText(str(value))
            
            # update database
            conn = connect('users.db')
            c = conn.cursor()
            c.execute(f'UPDATE {self.current_mode}_data SET {param}=? WHERE id=?', (value, self.id))
            conn.commit()
            c.close()

            # update board
            # send command to board to update parameter
            # updateBoard(self, param, value)

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
        # params = [(param, value), (param, value), ...] -> Can validate multiple inputs at once
        # check if inputs are valid, return true if inputs are valid, false if not
        for input in params:
            param = input[0]
            value = input[1]

            if param == 'lower_rate_limit': # value is in ppm
                # not in range
                if value < 30 or value > 175:
                    return False
                # in range but not a multiple of 5
                elif ((30 <= value and value <= 50) or (90 <= value and value <= 175)) and value % 5 != 0:
                    return False
                # in range but not a multiple of 10
                elif (50 < value and value < 90) and value % 1 != 0:
                    return False
                    
            elif param == 'upper_rate_limit' or param == 'max_sensor_rate': # value is in ppm
                # not in range
                if value < 50 or value > 175:
                    return False
                # in range but not a multiple of 5
                elif value % 5 != 0:
                    return False
                
            elif param == 'atrial_amplitude' or param == 'ventricular_amplitude': # value is in V
                # not in range              
                if value != 'Off' and (value < 0 or value > 5):
                    return False
                # in range but not a multiple of 0.1
                elif (0 < value and value < 5) and round(value % 0.1) != 0:
                    return False
                
            elif param == 'atrial_pulse_width' or param == 'ventricular_pulse_width': # value is in ms
                # not in range
                if value < 1 or value > 30:
                    return False
                # in range but not a multiple of 1
                elif value % 1 != 0:
                    return False
                
            elif param == 'ASens' or param == 'VSens': # value is in V
                # not in range
                if value < 0 or value > 5:
                    return False
                # in range but not a multiple of 0.1
                elif round(value % 0.1) != 0:
                    return False
                
            elif param == 'ARP' or param == 'VRP' or param == 'PVARP': # value is in ms
                # not in range
                if value < 150 or value > 500:
                    return False
                # in range but not a multiple of 10
                elif value % 10 != 0:
                    return False
                
            elif param == 'hysteresis': # value is 0 or 1, OFF or ON
                # not in range
                if value != 0 or value != 1:
                    return False
                
            elif param == 'activity_threshold': # represents a value; V-Low = 0, Low = 1, Med-Low = 2, Med = 3, Med-High = 4, High = 5, V-High = 6
                # not in range
                if value < 0 or value > 6:
                    return False
                # in range but not a multiple of 1
                elif value % 1 != 0:
                    return False
                
            elif param == 'reaction_time': # value is in seconds
                # not in range
                if value < 10 or value > 50:
                    return False
                # in range but not a multiple of 10
                elif value % 10 != 0:
                    return False
                
            elif param == 'response_factor': # no units of measurement
                # not in range
                if value < 1 or value > 16:
                    return False
                # in range but not a multiple of 1
                elif value % 1 != 0:
                    return False
                
            elif param == 'recovery_time': # value is in minutes
                # not in range
                if value < 2 or value > 16:
                    return False
                # in range but not a multiple of 1
                elif value % 1 != 0:
                    return False

        return True
 