from models.user import user as userModel
from services.userDBManager import userDBMan
from services.tokenmanager import tokenManager
import bcrypt

class authorisationManager:
    def __init__(self) -> None:
        self.userDBMan = userDBMan()
        self.tokenManager = tokenManager()

    def validateLogin(self, username, password, scope):
        user = self.userDBMan.getUserbyUsername(username)

        if user is None:
            return {'error': 'Invalid username or password'}
        
        hashed_password = user[2]
        check = bcrypt.checkpw(password.encode('utf-8'), hashed_password)

        if check:
            # generate acces token for user and scope
            # return acces token
            acces_token = self.tokenManager.GenerateAccessToken(user[0], scope)
            return {'acces_token': acces_token}
        else:
            return {'error': 'Invalid username or password'}
        
    
    def createUser(self, user: userModel, password):
        # generate salt
        salt = bcrypt.gensalt()

        # hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # create user in db with hashed password
        self.userDBMan.createUser(user.username, user.email, hashed_password)

        return True

    def validateToken(self, acces_token, scope):
        return self.tokenManager.ValidateAccessToken(acces_token, scope)
    
    def simpleValidateToken(self, acces_token):
        return self.tokenManager.SimpleValidateAccessToken(acces_token)
    