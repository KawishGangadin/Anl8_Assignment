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

    def getMembers(self):
        conn = None
        memberList = []
        privateKey = cryptoUtils.loadPrivateKey()
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM members"
            cursor.execute(query)
            members = cursor.fetchall()
            cursor.close()
            for member in members:
                data_to_bytes = list(map(bytes, member))
                decrypted_data = list(map(cryptoUtils.decryptWithPrivateKey, privateKey, data_to_bytes))
                decrypted_data = tuple(map(lambda s: s.decode('utf-8'), decrypted_data))
                memberList.append(decrypted_data)
            return memberList
                
        except sqlite3.Error as e:
            print("An error occurred while retrieving members:", e)
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

    def updateTraveller(self, old_license_number, **fields):
        conn = None
        try:
            if len(fields) == 0:
                return "OK"

            if not Validation.validateMultipleInputs(**fields):
                return "FAIL"

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            publicKey = cryptoUtils.loadPublicKey()
            privateKey = cryptoUtils.loadPrivateKey()

            cursor.execute("SELECT * FROM travellers")
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
            print("An error occurred while deleting the member:", e)
            return "FAIL"

        finally:
            if conn:
                conn.close()

    def getScooters(self):
        # TODO: test
        conn = None
        scooterList = []
        privateKey = cryptoUtils.loadPrivateKey()
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM scooters"
            cursor.execute(query)
            scooters = cursor.fetchall()
            cursor.close()
            for scooter in scooters:
                data_to_bytes = list(map(bytes, scooter))[1:]
                decrypted_data = [cryptoUtils.decryptWithPrivateKey(privateKey, s) for s in data_to_bytes]
                decrypted_data = tuple(map(lambda s: s.decode('utf-8'), decrypted_data))
                all_data = (scooter[0],) + decrypted_data
                scooterList.append(all_data)
            return scooterList
                
        except sqlite3.Error as e:
            print("An error occurred while retrieving scooter data:", e)
            return None
        finally:
            if conn:
                conn.close()

    def getScooterByAttribute(self, search_key):
        scooterList = self.getScooters()
        if search_key:
            return [s for s in scooterList if ([x for x in s if search_key.lower() in str(x).lower()])]
        else:
            return scooterList

    def getScooterByID(self, id):
        conn = None
        scooter = None
        privateKey = cryptoUtils.loadPrivateKey()
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM scooters WHERE id = ?"
            cursor.execute(query, (id,))
            scooter = cursor.fetchone()
            cursor.close()
            if scooter:
                data_to_bytes = list(map(bytes, scooter))[1:]
                decrypted_data = [cryptoUtils.decryptWithPrivateKey(privateKey, s) for s in data_to_bytes]
                decrypted_data = tuple(map(lambda s: s.decode('utf-8'), decrypted_data))
                all_data = (scooter[0],) + decrypted_data
                return all_data
            else:
                return None
                
        except sqlite3.Error as e:
            print("An error occurred while retrieving scooter data:", e)
            return None
        finally:
            if conn:
                conn.close()
            
        
    def createScooter(self, fields):
        # TODO: validate new scooter fields (do dit in users.py)
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = """
                INSERT INTO scooters (in_service_date, brand, model, serial_number, top_speed, battery_capacity, state_of_charge, target_soc_min, target_soc_max, latitude, longitude, out_of_service, mileage, last_maintenance_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            public_key = cryptoUtils.loadPublicKey()
            in_service_date = date.today().strftime("%Y-%m-%d")
            fields.append(in_service_date)
            scooterdata = tuple([cryptoUtils.encryptWithPublicKey(public_key, f) for f in fields])
            cursor.execute(query, (scooterdata))
            conn.commit()
            cursor.close()
            return "OK"
        except sqlite3.Error as e:
            return e
        finally:
            if conn:
                conn.close()
            

    def editScooter(self, id, newFields):
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = """ 
                UPDATE scooters SET in_service_date = ?, brand = ?, model = ?, serial_number = ?, top_speed = ?, battery_capacity = ?,
                state_of_charge = ?, target_soc_min = ?, target_soc_max = ?, latitude = ?, longitude = ?, out_of_service = ?,
                mileage = ?, last_maintenance_date = ? WHERE id = ?
            """
            public_key = cryptoUtils.loadPublicKey()
            encrypted = tuple([cryptoUtils.encryptWithPublicKey(public_key, f) for f in newFields])
            all_data = encrypted + (id,)
            cursor.execute(query, (all_data))
            conn.commit()
            cursor.close()
            return "OK"
        except sqlite3.Error as e:
            return e
        finally:
            if conn:
                conn.close()

    def deleteScooter(self):
        pass

