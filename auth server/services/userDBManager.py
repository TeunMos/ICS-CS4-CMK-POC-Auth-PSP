import sqlite3
import os

databaseFile = 'database.db'

class userDBMan:
    def __init__(self) -> None:
        # read from schema.sql
        if not os.path.isfile(databaseFile):
            conn = sqlite3.connect(databaseFile)
            c = conn.cursor()

            with open('schema.sql', 'r') as f:
                c.executescript(f.read())

            conn.close()


    def getUserbyUsername(self, username):
        conn = sqlite3.connect(databaseFile)
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE username=?', (username,))
        result = c.fetchone()

        conn.close()

        return result
    
    def getUserInfo(self, id):
        conn = sqlite3.connect(databaseFile)
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE id=?', (id,))
        result = c.fetchone()

        conn.close()

        return result
    
    def createUser(self, username, email, hashed_password):
        conn = sqlite3.connect(databaseFile)
        c = conn.cursor()

        c.execute('INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()

        conn.close()
    