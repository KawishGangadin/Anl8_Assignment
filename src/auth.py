from users import roles
from users import consultant
from users import systemAdministrator
from users import superAdministrator
from cryptoUtils import cryptoUtils
import sqlite3

class loginAuth:
    def __init__(self, db):
        self.db = db

    def loginFunc(self, encrypted_username, password):
        data = self.db.getUserData(encrypted_username)
        if data:
            storedPassword = data[4]  # Assuming hashedPassword is stored in the 5th column
            storedSalt = data[8]  # Assuming salt is stored in the 9th column
            if cryptoUtils.verifyPassword(password, storedPassword, storedSalt):
                private_key = cryptoUtils.loadPrivateKey()
                decrypted_username = cryptoUtils.decryptWithPrivateKey(private_key, data[3])  # Assuming encrypted username is in the 4th column
                decrypted_username = decrypted_username.decode('utf-8')
                decrypted_role = cryptoUtils.decryptWithPrivateKey(private_key, data[6])
                decrypted_role=decrypted_role.decode('utf-8')  # Assuming encrypted role is in the 7th column

                user_id = data[0]  # Assuming user_id is in the 1st column

                roleType = roles(decrypted_role)

                if roleType == roles.CONSULTANT:
                    return consultant(user_id, decrypted_username, self.db)  # Assuming consultant constructor takes user_id and username
                elif roleType == roles.ADMIN:
                    return systemAdministrator(user_id, decrypted_username, self.db)  # Assuming systemAdministrator constructor takes user_id and username
                elif roleType == roles.SUPERADMIN:
                    return superAdministrator(user_id, decrypted_username, self.db)  # Assuming superAdministrator constructor takes user_id and username
                else:
                    raise ValueError("Unknown role detected.")

        return None
