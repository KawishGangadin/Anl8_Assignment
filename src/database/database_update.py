from cryptoUtils import cryptoUtils
from inputValidation import Validation
import sqlite3

class DBUpdate:
    
    def updatePassword(self, userId, newPassword, temp=False):
        conn = None
        try:
            if Validation.passwordValidation(newPassword):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()

                hashed_password, salt = cryptoUtils.hashPassword(newPassword)

                temp_flag = 1 if temp else 0
                query = "UPDATE users SET password_hash = ?, temp = ?, salt = ?, session_id = session_id +1 WHERE id = ?"
                parameters = (hashed_password, temp_flag, salt, userId)

                cursor.execute(query, parameters)
                conn.commit()
                cursor.close()
                return "OK"
            else:
                return "FAIL"
        except sqlite3.Error as e:
            print("An error occurred while updating the password:", e)
            return None
        finally:
            if conn:
                conn.close()

    def updateUser(self, userId, firstName, lastName, username):
        conn = None
        try:
            validationData = { "first_name": firstName, "last_name": lastName, "username": username }
            if Validation.validateMultipleInputs(**validationData):
                conn = sqlite3.connect(self.databaseFile)
                privateKey = cryptoUtils.loadPrivateKey()
                publicKey = cryptoUtils.loadPublicKey()
                cursor = conn.cursor()
                query = """
                UPDATE users
                SET first_name = ?, last_name = ?, username = ?
                WHERE id = ?
                """
            
                if username:
                    encrypted_username = cryptoUtils.encryptWithPublicKey(publicKey, username)
                else:
                    encrypted_username = None
                
                parameters = (firstName, lastName, encrypted_username, userId)

                cursor.execute(query, parameters)
                
                if cursor.rowcount > 0:
                    result = "OK"
                else:
                    result = "FAIL"
                conn.commit() 
                
                cursor.close()
                return result
            return "FAIL"

        except sqlite3.Error as e:
            print("SQLite error:", e)
            return None

        except Exception as e:
            print("An error occurred while updating the user:", e)
            return None

        finally:
            if conn:
                conn.close()