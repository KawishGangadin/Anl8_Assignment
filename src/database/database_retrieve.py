from cryptoUtils import cryptoUtils
from inputValidation import Validation
from utility import Utility
import sqlite3
import time

class DBRetrieve:

    def getAllTravellers(self):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM travellers")
            results = cursor.fetchall()
            cursor.close()
            return results
        except sqlite3.Error as e:
            print("Error retrieving traveller records:", e)
            return []
        finally:
            if conn:
                conn.close()
    
    def getRestoreCodesByUser(self, user_id):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT code, backup_filename FROM restore_codes WHERE system_admin_id = ?"
            cursor.execute(query, (user_id,))
            codes = cursor.fetchall()
            cursor.close()
            return codes
        except sqlite3.Error as e:
            print("An error occurred while fetching restore codes:", e)
            return []
        finally:
            if conn:
                conn.close()
    
    def getUserData(self, username):
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
                        return user

                # print(f"User with username {username} not found.")
            return None

        except sqlite3.Error as e:
            print("An error occurred while retrieving user data:", e)
            return None
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
    
    def getUsers(self, role=None):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            query = "SELECT * FROM users"
            cursor.execute(query)

            users = cursor.fetchall()
            cursor.close()

            userList = []  # Initialize the userList here

            if role is not None:
                for user in users:
                    encrypted_role = user[6]
                    decrypted_role_bytes = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), encrypted_role).decode('utf-8')
                    if decrypted_role_bytes == role.value:
                        decryptedUsername = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), user[3]).decode('utf-8')
                        decryptedRole = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), user[6]).decode('utf-8')
                        hiddenPassword = "********"  # Assign hidden password here
                        decryptedUser = (
                            user[0],  # ID
                            user[1],  # First name
                            user[2],  # Last name
                            decryptedUsername,  # Decrypted username
                            hiddenPassword,  # Hidden password
                            user[5],  # Registration date
                            decryptedRole  # Decrypted role
                        )
                        userList.append(decryptedUser)

                return userList

            for user in users:
                decryptedUsername = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), user[3]).decode('utf-8')
                decryptedRole = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), user[6]).decode('utf-8')
                hiddenPassword = "********"  # Assign hidden password here
                decryptedUser = (
                    user[0],  # ID
                    user[1],  # First name
                    user[2],  # Last name
                    decryptedUsername,  # Decrypted username
                    hiddenPassword,  # Hidden password
                    user[5],  # Registration date
                    decryptedRole  # Decrypted role
                )
                userList.append(decryptedUser)

            return userList

        except sqlite3.Error as e:
            print("An error occurred while retrieving users:", e)
            return None

        finally:
            if conn:
                conn.close()
    
# Make sure this import exists if not already there

    def displayAllTravellers(self):
        travellers = self.getAllTravellers()

        print("\n======= Registered Travellers =======")
        for t in travellers:
            print(f"Name: {Utility.safe_decrypt(t[2])} {Utility.safe_decrypt(t[3])}")
            print(f"Birthdate: {t[4]}")
            print(f"Gender: {Utility.safe_decrypt(t[5])}")
            print(f"Street: {Utility.safe_decrypt(t[6])} {Utility.safe_decrypt(t[7])}")
            print(f"City: {Utility.safe_decrypt(t[8])}")
            print(f"Zip: {Utility.safe_decrypt(t[9])}")
            print(f"Email: {Utility.safe_decrypt(t[10])}")
            print(f"Mobile: {Utility.safe_decrypt(t[11])}")
            print(f"License: {Utility.safe_decrypt(t[12])}")
            print("-------------------------------------")

    def displayAllScooters(self):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scooters")
            scooters = cursor.fetchall()
            cursor.close()

            print("\n======= Registered Scooters =======")
            for s in scooters:
                print(f"ID: {s[1]}")
                print(f"Brand: {s[2]}")
                print(f"Model: {s[3]}")
                print(f"Serial Number: {Utility.safe_decrypt(s[4])}")
                print(f"Top Speed: {s[5]} km/h")
                print(f"Battery Capacity: {s[6]} Wh")
                print(f"SoC: {s[7]}%, Target Min: {s[8]}%, Target Max: {s[9]}%")
                print(f"Latitude: {Utility.safe_decrypt(s[10])}")
                print(f"Longitude: {Utility.safe_decrypt(s[11])}")
                print(f"Out of Service: {'Yes' if s[12] else 'No'}")
                print(f"Mileage: {s[13]} km")
                print(f"Last Maintenance: {s[14]}")
                print("-------------------------------------")

        except sqlite3.Error as e:
            print("An error occurred while retrieving scooters:", e)
        finally:
            if conn:
                conn.close()
