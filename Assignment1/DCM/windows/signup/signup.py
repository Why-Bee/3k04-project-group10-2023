from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

from sqlite3 import connect
from hashlib import sha256

from windows.landingpage.landingpage import LandingWindow


class SignupWindow(QMainWindow): 
    def __init__(self, stacked_window):
        super(SignupWindow, self).__init__()
        loadUi('./windows/signup/signup.ui', self)
        self.stacked_window = stacked_window
        self.stacked_window.setWindowTitle("Sign Up")
        self.backButton.clicked.connect(self.back_clicked) 
        self.signUpConfirm.clicked.connect(self.check_signup) 


    def back_clicked(self):
        self.stacked_window.setCurrentIndex(0) 
        # clear stack
        self.stacked_window.removeWidget(self.stacked_window.widget(1)) 
        self.stacked_window.setWindowTitle("Welcome")

    def check_signup(self):
        username = self.usernameField.text()
        password = self.passwordField.text()

        if (len(username) == 0 or len(password) == 0):
            self.errorLabel.setText('Please fill in all fields')

        else:
            # check if username is already in database
            conn = connect('users.db')
            c = conn.cursor()
            c.execute('SELECT * FROM all_users WHERE username=?', (username,))

            if (c.fetchone() == None):
               # check if password and confirm password match
                if (self.passwordField.text() == self.confirmPasswordField.text()):
                    # database cannot have more than 10 entries
                    c.execute('SELECT * FROM all_users')
                    if (len(c.fetchall()) >= 10):
                        self.errorLabel.setText('Database is full.')
                        return
                    

                    # add username and password to database after hashing password
                    password = sha256(password.encode()).hexdigest()
                    # note: table has a primary key, so we need to specify the columns
                    # fetch number of rows in table
                    c.execute('SELECT COUNT(id) FROM all_users')
                    global id
                    id = c.fetchone()[0] + 1
                    c.execute('INSERT INTO all_users (username, password, id) VALUES (?, ?, ?)', (username, password, id))
                    conn.commit()
                    c.close()
                    # add new programmable parameters to all tables
                    self.create_programmable_parameters(id)

                    # change the text to green
                    self.errorLabel.setStyleSheet('color: green')
                    self.errorLabel.setText('Sign up successful')
                    
                    QTimer.singleShot(1000, lambda: self.show_landing_window())
                else:
                    self.errorLabel.setText('Passwords do not match.')
            else:
                self.errorLabel.setText('Username already exists.')

    def create_programmable_parameters(self, id): # create programmable parameters for new user
        conn = connect('users.db')
        c = conn.cursor()
        # go through tables
        self.create_programmable_parameters_AOO(id, c)
        self.create_programmable_parameters_VOO(id, c)
        self.create_programmable_parameters_AAI(id, c)
        self.create_programmable_parameters_VVI(id, c)
        self.create_programmable_parameters_AOOR(id, c)
        self.create_programmable_parameters_VOOR(id, c)
        self.create_programmable_parameters_AAIR(id, c)
        self.create_programmable_parameters_VVIR(id, c)
        # commit changes
        conn.commit()
        c.close()

    def create_programmable_parameters_AOO(self, id, c): # create programmable parameters for new user
        c.execute('INSERT INTO AOO_data (id, lower_rate_limit, upper_rate_limit, atrial_amplitude, atrial_pulse_width) VALUES (?, ?, ?, ?, ?)', (id, 60, 120, 35, 4))

    def create_programmable_parameters_VOO(self, id, c): # create programmable parameters for new user
        c.execute('INSERT INTO VOO_data (id, lower_rate_limit, upper_rate_limit, ventricular_amplitude, ventricular_pulse_width) VALUES (?, ?, ?, ?, ?)', (id, 60, 120, 35, 4))



    def create_programmable_parameters_AAI(self, id, c): # create programmable parameters for new user
        c.execute('INSERT INTO AAI_data (id, lower_rate_limit, upper_rate_limit, atrial_amplitude, atrial_pulse_width, sensitivity, ARP, PVARP, hysteresis, rate_smoothing) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 35, 4, 75, 250, 250, 0, 0))
        # c.execute('INSERT INTO AAI_upper_rate_limit (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO AAI_atrial_amplitude (id, value) VALUES (?, ?)', (id, 35))
        # c.execute('INSERT INTO AAI_atrial_pulse_width (id, value) VALUES (?, ?)', (id, 4))
        # c.execute('INSERT INTO AAI_sensitivity (id, value) VALUES (?, ?)', (id, 75))
        # c.execute('INSERT INTO AAI_ARP (id, value) VALUES (?, ?)', (id, 250))
        # c.execute('INSERT INTO AAI_PVARP (id, value) VALUES (?, ?)', (id, 250))
        # c.execute('INSERT INTO AAI_hysteresis (id, value) VALUES (?, ?)', (id, 0))
        # c.execute('INSERT INTO AAI_rate_smoothing (id, value) VALUES (?, ?)', (id, 0))

    def create_programmable_parameters_VVI(self, id, c): # create programmable parameters for new user
        # c.execute('INSERT INTO VVI_lower_rate_limit (id, value) VALUES (?, ?)', (id, 60))
        # c.execute('INSERT INTO VVI_upper_rate_limit (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO VVI_ventricular_amplitude (id, value) VALUES (?, ?)', (id, 35))
        # c.execute('INSERT INTO VVI_ventricular_pulse_width (id, value) VALUES (?, ?)', (id, 4))
        # c.execute('INSERT INTO VVI_sensitivity (id, value) VALUES (?, ?)', (id, 250))
        # c.execute('INSERT INTO VVI_VRP (id, value) VALUES (?, ?)', (id, 320))
        # c.execute('INSERT INTO VVI_hysteresis (id, value) VALUES (?, ?)', (id, 0))
        # c.execute('INSERT INTO VVI_rate_smoothing (id, value) VALUES (?, ?)', (id, 0))
        c.execute('INSERT INTO VVI_data (id, lower_rate_limit, upper_rate_limit, ventricular_amplitude, ventricular_pulse_width, sensitivity, VRP, hysteresis, rate_smoothing) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 35, 4, 250, 320, 0, 0))

    def create_programmable_parameters_AOOR(self, id, c): # create programmable parameters for new user
        # c.execute('INSERT INTO AOOR_lower_rate_limit (id, value) VALUES (?, ?)', (id, 60))
        # c.execute('INSERT INTO AOOR_upper_rate_limit (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO AOOR_maximum_sensor_rate (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO AOOR_atrial_amplitude (id, value) VALUES (?, ?)', (id, 35))
        # c.execute('INSERT INTO AOOR_atrial_pulse_width (id, value) VALUES (?, ?)', (id, 4))
        # c.execute('INSERT INTO AOOR_activity_threshold (id, value) VALUES (?, ?)', (id, 3))
        # c.execute('INSERT INTO AOOR_reaction_time (id, value) VALUES (?, ?)', (id, 30))
        # c.execute('INSERT INTO AOOR_response_factor (id, value) VALUES (?, ?)', (id, 8))
        # c.execute('INSERT INTO AOOR_recovery_time (id, value) VALUES (?, ?)', (id, 5))
        c.execute('INSERT INTO AOOR_data (id, lower_rate_limit, upper_rate_limit, maximum_sensor_rate, atrial_amplitude, atrial_pulse_width, activity_threshold, reaction_time, response_factor, recovery_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4, 3, 30, 8, 5))

    def create_programmable_parameters_VOOR(self, id, c): # create programmable parameters for new user
        # c.execute('INSERT INTO VOOR_lower_rate_limit (id, value) VALUES (?, ?)', (id, 60))
        # c.execute('INSERT INTO VOOR_upper_rate_limit (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO VOOR_maximum_sensor_rate (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO VOOR_ventricular_amplitude (id, value) VALUES (?, ?)', (id, 35))
        # c.execute('INSERT INTO VOOR_ventricular_pulse_width (id, value) VALUES (?, ?)', (id, 4))
        # c.execute('INSERT INTO VOOR_activity_threshold (id, value) VALUES (?, ?)', (id, 3))
        # c.execute('INSERT INTO VOOR_reaction_time (id, value) VALUES (?, ?)', (id, 30))
        # c.execute('INSERT INTO VOOR_response_factor (id, value) VALUES (?, ?)', (id, 8))
        # c.execute('INSERT INTO VOOR_recovery_time (id, value) VALUES (?, ?)', (id, 5))
        c.execute('INSERT INTO VOOR_data (id, lower_rate_limit, upper_rate_limit, maximum_sensor_rate, ventricular_amplitude, ventricular_pulse_width, activity_threshold, reaction_time, response_factor, recovery_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4, 3, 30, 8, 5))

    def create_programmable_parameters_AAIR(self, id, c): # create programmable parameters for new user
        # c.execute('INSERT INTO AAIR_lower_rate_limit (id, value) VALUES (?, ?)', (id, 60))
        # c.execute('INSERT INTO AAIR_upper_rate_limit (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO AAIR_maximum_sensor_rate (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO AAIR_atrial_amplitude (id, value) VALUES (?, ?)', (id, 35))
        # c.execute('INSERT INTO AAIR_atrial_pulse_width (id, value) VALUES (?, ?)', (id, 4))
        # c.execute('INSERT INTO AAIR_sensitivity (id, value) VALUES (?, ?)', (id, 75))
        # c.execute('INSERT INTO AAIR_ARP (id, value) VALUES (?, ?)', (id, 250))
        # c.execute('INSERT INTO AAIR_PVARP (id, value) VALUES (?, ?)', (id, 250))
        # c.execute('INSERT INTO AAIR_hysteresis (id, value) VALUES (?, ?)', (id, 0))
        # c.execute('INSERT INTO AAIR_rate_smoothing (id, value) VALUES (?, ?)', (id, 0))
        # c.execute('INSERT INTO AAIR_activity_threshold (id, value) VALUES (?, ?)', (id, 3))
        # c.execute('INSERT INTO AAIR_reaction_time (id, value) VALUES (?, ?)', (id, 30))
        # c.execute('INSERT INTO AAIR_response_factor (id, value) VALUES (?, ?)', (id, 8))
        # c.execute('INSERT INTO AAIR_recovery_time (id, value) VALUES (?, ?)', (id, 5))
        c.execute('INSERT INTO AAIR_data (id, lower_rate_limit, upper_rate_limit, maximum_sensor_rate, atrial_amplitude, atrial_pulse_width, sensitivity, ARP, PVARP, hysteresis, rate_smoothing, activity_threshold, reaction_time, response_factor, recovery_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4, 75, 250, 250, 0, 0, 3, 30, 8, 5))
        
    def create_programmable_parameters_VVIR(self, id, c): # create programmable parameters for new user
        # c.execute('INSERT INTO VVIR_lower_rate_limit (id, value) VALUES (?, ?)', (id, 60))
        # c.execute('INSERT INTO VVIR_upper_rate_limit (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO VVIR_maximum_sensor_rate (id, value) VALUES (?, ?)', (id, 120))
        # c.execute('INSERT INTO VVIR_ventricular_amplitude (id, value) VALUES (?, ?)', (id, 35))
        # c.execute('INSERT INTO VVIR_ventricular_pulse_width (id, value) VALUES (?, ?)', (id, 4))
        # c.execute('INSERT INTO VVIR_sensitivity (id, value) VALUES (?, ?)', (id, 250))
        # c.execute('INSERT INTO VVIR_VRP (id, value) VALUES (?, ?)', (id, 320))
        # c.execute('INSERT INTO VVIR_hysteresis (id, value) VALUES (?, ?)', (id, 0))
        # c.execute('INSERT INTO VVIR_rate_smoothing (id, value) VALUES (?, ?)', (id, 0))
        # c.execute('INSERT INTO VVIR_activity_threshold (id, value) VALUES (?, ?)', (id, 3))
        # c.execute('INSERT INTO VVIR_reaction_time (id, value) VALUES (?, ?)', (id, 30))
        # c.execute('INSERT INTO VVIR_response_factor (id, value) VALUES (?, ?)', (id, 8))
        # c.execute('INSERT INTO VVIR_recovery_time (id, value) VALUES (?, ?)', (id, 5))
        c.execute('INSERT INTO VVIR_data (id, lower_rate_limit, upper_rate_limit, maximum_sensor_rate, ventricular_amplitude, ventricular_pulse_width, sensitivity, VRP, hysteresis, rate_smoothing, activity_threshold, reaction_time, response_factor, recovery_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4, 250, 320, 0, 0, 3, 30, 8, 5))

    def show_landing_window(self):
        landing_window = LandingWindow(self.stacked_window)
        self.stacked_window.addWidget(landing_window)
        self.stacked_window.setCurrentIndex(2)