import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('CREATE TABLE AOO_data (id INTEGER PRIMARY KEY AUTOINCREMENT, lower_rate_limit INTEGER, upper_rate_limit INTEGER, atrial_amplitude INTEGER, atrial_pulse_width INTEGER)')
c.execute('CREATE TABLE VOO_data (id INTEGER PRIMARY KEY AUTOINCREMENT, lower_rate_limit INTEGER, upper_rate_limit INTEGER, ventricular_amplitude INTEGER, ventricular_pulse_width INTEGER )')
c.execute('CREATE TABLE AAI_data (id INTEGER PRIMARY KEY AUTOINCREMENT, lower_rate_limit INTEGER, upper_rate_limit INTEGER, atrial_amplitude INTEGER, atrial_pulse_width INTEGER, sensitivity INTEGER, ARP INTEGER, PVARP INTEGER, hysteresis INTEGER, rate_smoothing INTEGER)')
c.execute('CREATE TABLE VVI_data (id INTEGER PRIMARY KEY AUTOINCREMENT, lower_rate_limit INTEGER, upper_rate_limit INTEGER, ventricular_amplitude INTEGER, ventricular_pulse_width INTEGER, sensitivity INTEGER, VRP INTEGER, hysteresis INTEGER, rate_smoothing INTEGER)')
c.execute('CREATE TABLE AOOR_data (id INTEGER PRIMARY KEY AUTOINCREMENT, lower_rate_limit INTEGER, upper_rate_limit INTEGER, maximum_sensor_rate INTEGER, atrial_amplitude INTEGER, atrial_pulse_width INTEGER, max_sensor_rate INTEGER, activity_threshold INTEGER, reaction_time INTEGER, response_factor INTEGER, recovery_time INTEGER)')
c.execute('CREATE TABLE VOOR_data (id INTEGER PRIMARY KEY AUTOINCREMENT, lower_rate_limit INTEGER, upper_rate_limit INTEGER, maximum_sensor_rate INTEGER, ventricular_amplitude INTEGER, ventricular_pulse_width INTEGER, max_sensor_rate INTEGER, activity_threshold INTEGER, reaction_time INTEGER, response_factor INTEGER, recovery_time INTEGER)')
c.execute('CREATE TABLE AAIR_data (id INTEGER PRIMARY KEY AUTOINCREMENT, lower_rate_limit INTEGER, upper_rate_limit INTEGER, maximum_sensor_rate INTEGER, atrial_amplitude INTEGER, atrial_pulse_width INTEGER, sensitivity INTEGER, ARP INTEGER, PVARP INTEGER, hysteresis INTEGER, rate_smoothing INTEGER, activity_threshold INTEGER, reaction_time INTEGER, response_factor INTEGER, recovery_time INTEGER)')
c.execute('CREATE TABLE VVIR_data (id INTEGER PRIMARY KEY AUTOINCREMENT, lower_rate_limit INTEGER, upper_rate_limit INTEGER, maximum_sensor_rate INTEGER, ventricular_amplitude INTEGER, ventricular_pulse_width INTEGER, sensitivity INTEGER, VRP INTEGER, hysteresis INTEGER, rate_smoothing INTEGER, activity_threshold INTEGER, reaction_time INTEGER, response_factor INTEGER, recovery_time INTEGER)')

conn.commit()
c.close()
conn.close()
