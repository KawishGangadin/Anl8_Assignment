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
    
    def updateScooter(self, scooter_id, updates: dict):
        conn = None
        try:
            if not updates:
                print("No fields to update.")
                return "OK"

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM scooters WHERE id = ?", (scooter_id,))
            if not cursor.fetchone():
                print("Scooter not found.")
                return "FAIL"

            allowed_fields = [
                "brand", "model", "serial_number", "top_speed", "battery_capacity",
                "state_of_charge", "target_soc_min", "target_soc_max", "latitude",
                "longitude", "mileage", "last_maintenance_date"
            ]

            updates = {k: v for k, v in updates.items() if k in allowed_fields}
            if not updates:
                print("No valid fields provided.")
                return "FAIL"

            public_key = cryptoUtils.loadPublicKey()
            encrypted_updates = {}

            for key, value in updates.items():
                if key in ["serial_number", "latitude", "longitude"]:
                    encrypted_updates[key] = cryptoUtils.encryptWithPublicKey(public_key, str(value))
                else:
                    encrypted_updates[key] = value

            query = "UPDATE scooters SET " + ", ".join(f"{k} = ?" for k in encrypted_updates.keys())
            query += " WHERE id = ?"
            parameters = list(encrypted_updates.values()) + [scooter_id]

            cursor.execute(query, parameters)
            conn.commit()
            return "OK" if cursor.rowcount > 0 else "FAIL"

        except sqlite3.Error as e:
            print("An error occurred while updating the scooter:", e)
            return "FAIL"
        finally:
            if conn:
                conn.close()

    def updateTraveller(self, traveller_id, updates: dict):
        conn = None
        try:
            if not updates:
                print("No fields to update.")
                return "OK"

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM travellers WHERE customer_id = ?", (traveller_id,))
            if not cursor.fetchone():
                print("Traveller not found.")
                return "FAIL"

            public_key = cryptoUtils.loadPublicKey()
            encrypted_updates = {}
            for key, value in updates.items():
                if key in ["first_name", "last_name", "gender", "street_name", "house_number", "city", "zip_code", "email", "mobile", "license_number"]:
                    encrypted_updates[key] = cryptoUtils.encryptWithPublicKey(public_key, str(value))
                else:
                    encrypted_updates[key] = value

            query = "UPDATE travellers SET " + ", ".join(f"{k} = ?" for k in encrypted_updates.keys())
            query += " WHERE customer_id = ?"
            parameters = list(encrypted_updates.values()) + [traveller_id]

            cursor.execute(query, parameters)
            conn.commit()
            return "OK" if cursor.rowcount > 0 else "FAIL"

        except sqlite3.Error as e:
            print("An error occurred while updating the traveller:", e)
            return "FAIL"
        finally:
            if conn:
                conn.close()