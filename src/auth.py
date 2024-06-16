from users import roles
from users import consultant
from users import systemAdministrator
from users import superAdministrator
from cryptoUtils import cryptoUtils
import sqlite3

class loginAuth:
    def __init__(self, db):
        self.db = db

    def loginFunc(self, username, password):
        data = self.db.getUserData(username)
        if data:
            storedPassword = data[4]  # Assuming hashedPassword is stored in the 5th column
            storedSalt = data[8]  # Assuming salt is stored in the 9th column
            if cryptoUtils.verifyPassword(password, storedPassword, storedSalt):
                role = data[6]  # Assuming data[6] contains the role identifier
                user_id = data[0]  # Assuming data[0] contains the user ID
                username = data[3]  # Assuming data[1] contains the username

                roleType = roles(role)
            if roleType == roles.CONSULTANT:
                return consultant(user_id, username,self.db)  # Assuming consultant constructor takes user_id and username
            elif roleType == roles.ADMIN:
                return systemAdministrator(user_id, username,self.db)  # Assuming systemAdministrator constructor takes user_id and username
            elif roleType == roles.SUPERADMIN:
                return superAdministrator(user_id, username,self.db)  # Assuming superAdministrator constructor takes user_id and username
            else:
                raise ValueError("Unknown role detected.")
        
        return None  # Return None if login fails or data is None
