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

    conn.commit()
    c.close()
