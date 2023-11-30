from hashlib import sha256
from sqlite3 import connect

from windows.landingpage.landingpage import MODES
from windows.signup.signup import MAX_USERS


# Fill the rest of the database with dummy data
# Used for testing purposes
def fill_database():
    conn = connect('./users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM all_users')
    data = c.fetchall()

    for i in range(len(data)+1, MAX_USERS+1):
        username = 'user' + str(i)
        password = sha256('pass'.encode()).hexdigest()
        c.execute('INSERT INTO all_users (username, password, id, notes) VALUES (?, ?, ?, ?)', (username, password, i, ""))
        for mode in MODES:
            c.execute(f'INSERT INTO {mode}_data (id) VALUES (?)', (i,))
            for param in MODES[mode]:
                c.execute(f'UPDATE {mode}_data SET {param} = ? WHERE id = ?', (0, i))

    # commit changes
    conn.commit()
    c.close()

# def create_programmable_parameters_AOO(id, c): # create programmable parameters for new user
#     c.execute('INSERT INTO AOO_data (id, lower_rate_limit, upper_rate_limit, atrial_amplitude, atrial_pulse_width) VALUES (?, ?, ?, ?, ?)', (id, 60, 120, 35, 4))

# def create_programmable_parameters_VOO(id, c): # create programmable parameters for new user
#     c.execute('INSERT INTO VOO_data (id, lower_rate_limit, upper_rate_limit, ventricular_amplitude, ventricular_pulse_width) VALUES (?, ?, ?, ?, ?)', (id, 60, 120, 35, 4))

# def create_programmable_parameters_AAI(id, c): # create programmable parameters for new user
#     c.execute('INSERT INTO AAI_data (id, lower_rate_limit, upper_rate_limit, atrial_amplitude, atrial_pulse_width, atrial_sensitivity, ARP, PVARP, hysteresis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 35, 4, 75, 250, 250, 0))

# def create_programmable_parameters_VVI(id, c): # create programmable parameters for new user
#     c.execute('INSERT INTO VVI_data (id, lower_rate_limit, upper_rate_limit, ventricular_amplitude, ventricular_pulse_width, ventricular_sensitivity, VRP, hysteresis) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 35, 4, 250, 320, 0))

# def create_programmable_parameters_AOOR(id, c): # create programmable parameters for new user
#     c.execute('INSERT INTO AOOR_data (id, lower_rate_limit, upper_rate_limit, max_sensor_rate, atrial_amplitude, atrial_pulse_width) VALUES (?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4))

# def create_programmable_parameters_VOOR(id, c): # create programmable parameters for new user
#     c.execute('INSERT INTO VOOR_data (id, lower_rate_limit, upper_rate_limit, max_sensor_rate, ventricular_amplitude, ventricular_pulse_width) VALUES (?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4))

# def create_programmable_parameters_AAIR(id, c): # create programmable parameters for new user
#     c.execute('INSERT INTO AAIR_data (id, lower_rate_limit, upper_rate_limit, max_sensor_rate, atrial_amplitude, atrial_pulse_width, atrial_sensitivity, ARP, PVARP, hysteresis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4, 75, 250, 250, 0))
    
# def create_programmable_parameters_VVIR(id, c): # create programmable parameters for new user
#     c.execute('INSERT INTO VVIR_data (id, lower_rate_limit, upper_rate_limit, max_sensor_rate, ventricular_amplitude, ventricular_pulse_width, ventricular_sensitivity, VRP, hysteresis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, 60, 120, 120, 35, 4, 250, 320, 0))
