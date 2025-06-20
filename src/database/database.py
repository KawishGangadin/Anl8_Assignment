from datetime import date
import sqlite3
from sqlite3 import Error
from roles import roles
from cryptoUtils import cryptoUtils
from inputValidation import Validation
from .database_create import DBCreate
from .database_update import DBUpdate
from .database_delete import DBDelete
from .database_retrieve import DBRetrieve
import secrets
import string
import os
import time


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
                if decrypted_role == b"superadmin":
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
                    if decrypted_role.decode('utf-8') == role.value:
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
                decrypted = cryptoUtils.decryptWithPrivateKey(private_key, record[0]).decode()
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
                query = "SELECT * FROM users WHERE session_id = ? AND id = ?"
                cursor.execute(query, (session_id,user_id))
                users = cursor.fetchone()
                cursor.close()

                if users:
                    return True
                else:
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
                    decrypted_username = decrypted_username_bytes.decode('utf-8') 
                    
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
                    decrypted_id = cryptoUtils.decryptWithPrivateKey(private_key, encrypted_cust_id).decode()
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