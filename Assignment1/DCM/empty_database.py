from sqlite3 import connect

from windows.landingpage.landingpage import MODES


# Empty the database except admin user
# Used for testing purposes
def empty_database():
    conn = connect('./users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM all_users')
    users = c.fetchall()

    for i in range (2, len(users)+1):
        id = i
        
        c.execute('DELETE FROM all_users WHERE id = ?', (id,))
        for mode in MODES:
            c.execute(f'DELETE FROM {mode}_data WHERE id = ?', (id,))
        
    conn.commit()
    conn.close()
    