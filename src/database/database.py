from datetime import date
import sqlite3
from utility import Utility
from cryptoUtils import CryptoUtils
from inputValidation import InputValidation
from .database_create import DBCreate
from .database_update import DBUpdate
from .database_delete import DBDelete
from .database_retrieve import DBRetrieve
from .authorization import Authorization

class DB(DBUpdate, DBCreate, DBRetrieve, DBDelete, Authorization):
    def __init__(self, databaseFile) -> None:
        self.databaseFile = databaseFile
    
    def InitSuperadmin(self):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            public_key = CryptoUtils.LoadPublicKey()
            private_key = CryptoUtils.LoadPrivateKey()

            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

            superadmin_exists = False

            for user in users:
                decrypted_role = CryptoUtils.DecryptWithPrivateKey(private_key, user[6])  
                if decrypted_role == "superadmin":
                    superadmin_exists = True
                    break

            if superadmin_exists:
                print("Superadmin already exists.")
            else:
                hashed_password, salt = CryptoUtils.HashPassword("Admin_123?")
                encrypted_username = CryptoUtils.EncryptWithPublicKey(public_key, "super_admin")
                encrypted_role = CryptoUtils.EncryptWithPublicKey(public_key, "superadmin")

                query = """
                INSERT INTO users (first_name, last_name, username, password_hash, registration_date, role, temp, salt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                registration_date = date.today().strftime("%Y-%m-%d")
                parameters = ("Kawish", "Gangadin", encrypted_username, hashed_password, registration_date, encrypted_role, 0, salt)

                cursor.execute(query, parameters)
                conn.commit()
                print("Superadmin initialized successfully.")
        except sqlite3.Error as e:
            print("An error occurred while initializing superadmin:", e)
            conn.close()
        finally:
            if conn:
                conn.close()

    def FindUserID(self, user_id, role):
        conn = None
        try:
            if str(user_id).isdigit():
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM users"
                cursor.execute(query)
                users = cursor.fetchall()
                cursor.close()

                private_key = CryptoUtils.LoadPrivateKey()  
                decrypted_role = None

                for user in users:
                    decrypted_role = CryptoUtils.DecryptWithPrivateKey(private_key, user[6])  
                    if decrypted_role == role.value:
                        if user[0] == user_id:
                            return True 

            return False  
        except sqlite3.Error as e:
            print("An error occurred while searching for user ID:", e)
            return False
        finally:
            if conn:
                conn.close()

    def LicenseExists(self, license_number):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT license_number FROM travellers")
            records = cursor.fetchall()
            private_key = CryptoUtils.LoadPrivateKey()
            for record in records:
                decrypted = CryptoUtils.DecryptWithPrivateKey(private_key, record[0])
                if decrypted == license_number:
                    return True
            return False
        except Exception as e:
            print("Error while checking license:", e)
            return False
        finally:
            if conn:
                conn.close()

    def ValidateSession(self, user_id,session_id,user_role):
        conn = None
        try:
            if str(user_id).isdigit():
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM users WHERE id = ?"
                cursor.execute(query, (user_id,))
                user = cursor.fetchone()
                cursor.close()

                if user:
                    decryptedUserRole = Utility.SafeDecrypt(user[6])
                    decryptedSessionID = Utility.SafeDecrypt(user[9])
                    if decryptedSessionID == str(session_id) and decryptedUserRole == user_role.value:
                        return True
                return False

            return False  

        except sqlite3.Error as e:
            print("An error occurred while validating login:", e)
            return False
        finally:
            if conn:
                conn.close()

    def FindUsername(self, username):
        conn = None
        try:
            if InputValidation.ValidateUsername(username):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM users"
                cursor.execute(query)
                
                users = cursor.fetchall()
                cursor.close()
                
                private_key = CryptoUtils.LoadPrivateKey()
                
                for user in users:
                    decrypted_username_bytes = CryptoUtils.DecryptWithPrivateKey(private_key, user[3])
                    decrypted_username = decrypted_username_bytes
                    
                    if decrypted_username == username:
                        return True
            return False
        
        except sqlite3.Error as e:
            print("An error occurred while searching for username:", e)
            return False
        finally:
            if conn:
                conn.close()

    def FindTravellerID(self, customer_id):
        conn = None
        try:
            private_key = CryptoUtils.LoadPrivateKey()

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id FROM travellers")
            travellers = cursor.fetchall()
            cursor.close()

            for encrypted_cust_id, in travellers:
                try:
                    decrypted_id = CryptoUtils.DecryptWithPrivateKey(private_key, encrypted_cust_id)
                    if decrypted_id == customer_id:
                        return True
                except Exception:
                    continue

            return False

        except sqlite3.Error as e:
            print("An error occurred while searching for traveller ID:", e)
            return False
        finally:
            if conn:
                conn.close()

    def GetUsernameByID(self, user_id):
        conn = None
        try:
            if(str(user_id).isdigit()):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT username FROM users WHERE id = ?"
                cursor.execute(query, (user_id,))
                username = cursor.fetchone()
                cursor.close()
                return CryptoUtils.DecryptWithPrivateKey(CryptoUtils.LoadPrivateKey(),username[0]) if username else None
            return None
        except sqlite3.Error as e:
            print("An error occurred while retrieving username by user ID:", e)
            return None
        finally:
            if conn:
                conn.close()

    def VerifyUserLogin(self,username, password):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            verifiedUser = None
            for user in users:
                if Utility.SafeDecrypt(user[3]) == username and CryptoUtils.VerifyPassword(password,user[4],user[8]):
                    verifiedUser = user
                    break

            if verifiedUser:
                new_session_id = Utility.GenerateSessionID()
                encrypted_session_id = CryptoUtils.EncryptWithPublicKey(CryptoUtils.LoadPublicKey(),new_session_id)

                # Step 3: Update session ID in DB
                update_query = "UPDATE users SET session_id = ? WHERE id = ?"
                cursor.execute(update_query, (encrypted_session_id, verifiedUser[0]))

                # Step 4: Check if update was successful
                if cursor.rowcount == 1:
                    conn.commit()
                    # Step 5: Return decrypted user
                    return {
                        'id': verifiedUser[0],
                        'role': Utility.SafeDecrypt(verifiedUser[6]),
                        'username': Utility.SafeDecrypt(verifiedUser[3]),
                        'sessionID': new_session_id  # Plaintext session ID for current session
                    }

            return None 
        except sqlite3.Error as e:
            return None
        finally:
            if conn:
                conn.close()
        
    def VerifyAccountStatus(self,userID, sessionID):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query,(userID,))
            user = cursor.fetchone()

            if user:
                decryptedSessionID = Utility.SafeDecrypt(user[9])
                if str(sessionID) == decryptedSessionID:
                     return user[7] == 1
            return None
        except Exception as e:
            print(f"Something went wrong while verifying the account status: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def ClearSession(self, userID,sessionID):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query,(userID,))
            user = cursor.fetchone()
            if Utility.SafeDecrypt(user[9]) == sessionID:
                update_query = "UPDATE users SET session_id = NULL WHERE id = ?"
                cursor.execute(update_query, (userID,))

                if cursor.rowcount == 1:
                    conn.commit()
                    print("Session ID cleared!!!")
                    return "OK"
            return None
        except Exception as e:
            print(f"Something went wrong while clearing sessionID")
            return None
        finally:
            if conn:
                conn.close()
    
    def ClearAllSessions(self):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            update_query = "UPDATE users SET session_id = NULL"
            cursor.execute(update_query)

            conn.commit()
            return "OK"
        except Exception as e:
            print(f"Something went wrong while clearing all session IDs: {e}")
            return None
        finally:
            if conn:
                conn.close()
