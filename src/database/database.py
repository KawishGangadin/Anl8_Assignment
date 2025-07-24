from datetime import date
import sqlite3
from utility import Utility
from cryptoUtils import cryptoUtils
from inputValidation import Validation
from .database_create import DBCreate
from .database_update import DBUpdate
from .database_delete import DBDelete
from .database_retrieve import DBRetrieve


class DB(DBUpdate, DBCreate, DBRetrieve, DBDelete):
    def __init__(self, databaseFile) -> None:
        self.databaseFile = databaseFile
    
    def initSuperadmin(self):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            public_key = cryptoUtils.loadPublicKey()
            private_key = cryptoUtils.loadPrivateKey()

            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

            superadmin_exists = False

            for user in users:
                decrypted_role = cryptoUtils.decryptWithPrivateKey(private_key, user[6])  
                if decrypted_role == "superadmin":
                    superadmin_exists = True
                    break

            if superadmin_exists:
                print("Superadmin already exists.")
            else:
                hashed_password, salt = cryptoUtils.hashPassword("Admin_123?")
                encrypted_username = cryptoUtils.encryptWithPublicKey(public_key, "super_admin")
                encrypted_role = cryptoUtils.encryptWithPublicKey(public_key, "superadmin")

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

    def findUserID(self, user_id, role):
        conn = None
        try:
            if str(user_id).isdigit():
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM users"
                cursor.execute(query)
                users = cursor.fetchall()
                cursor.close()

                private_key = cryptoUtils.loadPrivateKey()  
                decrypted_role = None

                for user in users:
                    decrypted_role = cryptoUtils.decryptWithPrivateKey(private_key, user[6])  
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

    def licenseExists(self, license_number):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT license_number FROM travellers")
            records = cursor.fetchall()
            private_key = cryptoUtils.loadPrivateKey()
            for record in records:
                decrypted = cryptoUtils.decryptWithPrivateKey(private_key, record[0])
                if decrypted == license_number:
                    return True
            return False
        except Exception as e:
            print("Error while checking license:", e)
            return False
        finally:
            if conn:
                conn.close()

    def validateSession(self, user_id,session_id):
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
                    decryptedSessionID = Utility.safe_decrypt(user[9])
                    if decryptedSessionID == str(session_id):
                        return True
                return False

            return False  

        except sqlite3.Error as e:
            print("An error occurred while validating login:", e)
            return False
        finally:
            if conn:
                conn.close()

    def findUsername(self, username):
        conn = None
        try:
            if Validation.usernameValidation(username):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM users"
                cursor.execute(query)
                
                users = cursor.fetchall()
                cursor.close()
                
                private_key = cryptoUtils.loadPrivateKey()
                
                for user in users:
                    decrypted_username_bytes = cryptoUtils.decryptWithPrivateKey(private_key, user[3])
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

    def findTravellerID(self, customer_id):
        conn = None
        try:
            private_key = cryptoUtils.loadPrivateKey()

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id FROM travellers")
            travellers = cursor.fetchall()
            cursor.close()

            for encrypted_cust_id, in travellers:
                try:
                    decrypted_id = cryptoUtils.decryptWithPrivateKey(private_key, encrypted_cust_id)
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

    def getUsernameByID(self, user_id):
        conn = None
        try:
            if(str(user_id).isdigit()):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT username FROM users WHERE id = ?"
                cursor.execute(query, (user_id,))
                username = cursor.fetchone()
                cursor.close()
                return cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(),username[0]) if username else None
            return None
        except sqlite3.Error as e:
            print("An error occurred while retrieving username by user ID:", e)
            return None
        finally:
            if conn:
                conn.close()

    def verifyUserLogin(self,username, password):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            verifiedUser = None
            for user in users:
                if Utility.safe_decrypt(user[3]) == username and cryptoUtils.verifyPassword(password,user[4],user[8]):
                    verifiedUser = user
                    break

            if verifiedUser:
                new_session_id = Utility.generate_session_id()
                encrypted_session_id = cryptoUtils.encryptWithPublicKey(cryptoUtils.loadPublicKey(),new_session_id)

                # Step 3: Update session ID in DB
                update_query = "UPDATE users SET session_id = ? WHERE id = ?"
                cursor.execute(update_query, (encrypted_session_id, verifiedUser[0]))

                # Step 4: Check if update was successful
                if cursor.rowcount == 1:
                    conn.commit()
                    # Step 5: Return decrypted user
                    return {
                        'id': verifiedUser[0],
                        'role': Utility.safe_decrypt(verifiedUser[6]),
                        'username': Utility.safe_decrypt(verifiedUser[3]),
                        'sessionID': new_session_id  # Plaintext session ID for current session
                    }

            return None 
        except sqlite3.Error as e:
            return None
        finally:
            if conn:
                conn.close()

    def verifyAccountStatus(self,userID, sessionID):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query,(userID,))
            user = cursor.fetchone()

            if user:
                decryptedSessionID = Utility.safe_decrypt(user[9])
                if str(sessionID) == decryptedSessionID:
                     return user[7] == 1
            return None
        except Exception as e:
            print(f"Something went wrong while verifying the account status: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    def clearSession(self, userID,sessionID):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query,(userID,))
            user = cursor.fetchone()
            if Utility.safe_decrypt(user[9]) == sessionID:
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
    
    def clearAllSessions(self):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            # Set all session IDs to NULL
            update_query = "UPDATE users SET session_id = NULL"
            cursor.execute(update_query)

            conn.commit()
            print("✅ All session IDs cleared.")
            return "OK"
        except Exception as e:
            print(f"❌ Something went wrong while clearing all session IDs: {e}")
            return None
        finally:
            if conn:
                conn.close()
