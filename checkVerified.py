import sqlite3

def isVerified(phoneNumber):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    phoneNumber TEXT PRIMARY KEY,
                    verified INTEGER)''')

    c.execute("SELECT verified FROM users WHERE phoneNumber=?", (phoneNumber,))
    result = c.fetchone()
    if result is None:
        return False
    else:
        return True
    
def setVerified(isverified, phoneNumber):
    if not isverified:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (phoneNumber, verified) VALUES (?, 1)", (phoneNumber,))
        conn.commit()

