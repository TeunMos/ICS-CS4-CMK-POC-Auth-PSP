import sqlite3
from services.userDBManager import userDBMan, databaseFile
from models.user import user
import secrets
import time
import jwt

expirationtime = 3600 # 1 hour in seconds 

secret_key = 'secret'

class tokenManager:
    def __init__(self) -> None:
        self.userDBMan = userDBMan()

    def GenerateAccessToken(self, user_id, scope):
        random_string = secrets.token_hex(64)

        # save acces token in db
        conn = sqlite3.connect(databaseFile)
        c = conn.cursor()

        c.execute('INSERT INTO acces_tokens (token, user_id, scope) VALUES (?, ?, ?)', (random_string, user_id, scope))
        conn.commit()

        conn.close()

        return random_string
    
    def ValidateAccessToken(self, acces_token, scope):
        # check if acces token is in db
        conn = sqlite3.connect(databaseFile)
        c = conn.cursor()

        c.execute('SELECT * FROM acces_tokens WHERE token=?', (acces_token,))
        result = c.fetchone()

        conn.close()

        if result is None:
            return False
        
        # check if scope is correct
        if result[3] != scope:
            return False
        
        # check if acces token is expired
        created_at = result[4]

        # check if acces token is older than the expiration time
        if created_at + expirationtime < int(time.time()):
            return False
        
        return True
    
    def SimpleValidateAccessToken(self, acces_token):
        # check if acces token is in db
        conn = sqlite3.connect(databaseFile)
        c = conn.cursor()

        c.execute('SELECT * FROM acces_tokens WHERE token=?', (acces_token,))
        result = c.fetchone()

        conn.close()

        if result is None:
            return False
        
        # check if acces token is expired
        created_at = result[4]

        # check if acces token is older than the expiration time
        if created_at + expirationtime < int(time.time()):
            return False
        
        return True

    def GenerateIDToken(self, user:user, scope, acces_token):
        # generate id token
        id_token = {
            'sub': user.id,
            'name': user.username,
            'email': user.email,
            'scope': scope,
            'acces_token': acces_token
        }

        # convert to jwt
        jwt_token = jwt.encode(id_token, secret_key, algorithm='HS256')

        return jwt_token

    def DecodeIDToken(self, IDToken):
        return jwt.decode(IDToken, secret_key, algorithms=['HS256'])
        



