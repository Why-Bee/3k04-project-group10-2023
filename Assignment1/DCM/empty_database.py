from sqlite3 import connect

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
        c.execute('DELETE FROM AOO_data WHERE id = ?', (id,))
        c.execute('DELETE FROM VOO_data WHERE id = ?', (id,))
        c.execute('DELETE FROM AAI_data WHERE id = ?', (id,))
        c.execute('DELETE FROM VVI_data WHERE id = ?', (id,))
        c.execute('DELETE FROM AOOR_data WHERE id = ?', (id,))
        c.execute('DELETE FROM VOOR_data WHERE id = ?', (id,))
        c.execute('DELETE FROM AAIR_data WHERE id = ?', (id,))
        c.execute('DELETE FROM VVIR_data WHERE id = ?', (id,))
        
    conn.commit()
    conn.close()
    