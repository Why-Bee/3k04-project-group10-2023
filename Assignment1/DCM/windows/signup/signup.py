from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

from sqlite3 import connect
from hashlib import sha256

from windows.landingpage.landingpage import LandingWindow

MAX_USERS = 10

class SignupWindow(QMainWindow): 
    def __init__(self, stacked_window):
        super(SignupWindow, self).__init__()
        loadUi('./windows/signup/signup.ui', self)
        self.stacked_window = stacked_window
        self.stacked_window.setWindowTitle("Sign Up")
        self.backButton.clicked.connect(self.back_clicked) 
        self.signUpConfirm.clicked.connect(self.check_signup) 

        # Initialize id variable
        self.id = None


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
                    if (len(c.fetchall()) >= MAX_USERS):
                        self.errorLabel.setText('Database is full.')
                        return
                    

                    # add username and password to database after hashing password
                    password = sha256(password.encode()).hexdigest()
                    # note: table has a primary key, so we need to specify the columns
                    # fetch number of rows in table
                    c.execute('SELECT id FROM all_users')
                    data = c.fetchall()
                    # find first available id
                    for i in range(1, MAX_USERS+1):
                        if i >= len(data)+1 or data[i-1][0] != i:
                            self.id = i
                            break
                    c.execute('INSERT INTO all_users (username, password, id, notes) VALUES (?, ?, ?, ?)', (username, password, self.id, ""))
                    conn.commit()
                    c.close()
                    # add new programmable parameters to all tables
                    self.create_programmable_parameters()

                    # change the text to green
                    self.errorLabel.setStyleSheet('color: green')
                    self.errorLabel.setText('Sign up successful')
                    
                    QTimer.singleShot(1000, lambda: self.show_landing_window())
                else:
                    self.errorLabel.setText('Passwords do not match.')
            else:
                self.errorLabel.setText('Username already exists.')

    def create_programmable_parameters(self): # create programmable parameters for new user
        id = self.id
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

    def create_programmable_parameters_AOO(self, id, c):
        c.execute('INSERT INTO AOO_data (id, lower_rate_limit, upper_rate_limit, atrial_amplitude, atrial_pulse_width) VALUES (?, ?, ?, ?, ?)', (id, 60, 120, 35, 4))

    def create_programmable_parameters_VOO(self, id, c):
        c.execute('INSERT INTO VOO_data (id, lower_rate_limit, upper_rate_limit, ventricular_amplitude, ventricular_pulse_width) VALUES (?, ?, ?, ?, ?)', (id, 60, 120, 35, 4))

    def create_programmable_parameters_AAI(self, id, c):
        c.execute('INSERT INTO AAI_data (id, lower_rate_limit, upper_rate_limit, atrial_amplitude, atrial_pulse_width, atrial_sensitivity, ARP, PVARP, hysteresis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 35, 4, 75, 250, 250, 0))

    def create_programmable_parameters_VVI(self, id, c):
        c.execute('INSERT INTO VVI_data (id, lower_rate_limit, upper_rate_limit, ventricular_amplitude, ventricular_pulse_width, ventricular_sensitivity, VRP, hysteresis) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 35, 4, 250, 320, 0))

    def create_programmable_parameters_AOOR(self, id, c):
        c.execute('INSERT INTO AOOR_data (id, lower_rate_limit, upper_rate_limit, max_sensor_rate, atrial_amplitude, atrial_pulse_width) VALUES (?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4))

    def create_programmable_parameters_VOOR(self, id, c):
        c.execute('INSERT INTO VOOR_data (id, lower_rate_limit, upper_rate_limit, max_sensor_rate, ventricular_amplitude, ventricular_pulse_width) VALUES (?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4))

    def create_programmable_parameters_AAIR(self, id, c):
        c.execute('INSERT INTO AAIR_data (id, lower_rate_limit, upper_rate_limit, max_sensor_rate, atrial_amplitude, atrial_pulse_width, atrial_sensitivity, ARP, PVARP, hysteresis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4, 75, 250, 250, 0))
        
    def create_programmable_parameters_VVIR(self, id, c): # 
        c.execute('INSERT INTO VVIR_data (id, lower_rate_limit, upper_rate_limit, max_sensor_rate, ventricular_amplitude, ventricular_pulse_width, ventricular_sensitivity, VRP, hysteresis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4, 250, 320, 0))

    def show_landing_window(self):
        landing_window = LandingWindow(self.stacked_window, self.id)
        self.stacked_window.addWidget(landing_window)
        self.stacked_window.setCurrentIndex(2)
