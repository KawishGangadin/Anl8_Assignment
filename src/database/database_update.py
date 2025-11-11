from cryptoUtils import CryptoUtils
from utility import Utility
from inputValidation import InputValidation
import sqlite3

class DBUpdate:
    
    def UpdatePassword(self, userId, newPassword, userContext, temp=False, session=False,):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return "FAIL"
            if InputValidation.ValidatePassword(newPassword):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()

                hashed_password, salt = CryptoUtils.HashPassword(newPassword)

                temp_flag = 1 if temp else 0
                query = "UPDATE users SET password_hash = ?, temp = ?, salt = ? WHERE id = ?"
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

    def UpdateUser(self, userId, firstName, lastName, username, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return "FAIL"
            validationData = { "first_name": firstName, "last_name": lastName, "username": username }
            if InputValidation.ValidateUserInformation(**validationData):
                conn = sqlite3.connect(self.databaseFile)
                publicKey = CryptoUtils.LoadPublicKey()
                cursor = conn.cursor()
                query = """
                UPDATE users
                SET first_name = ?, last_name = ?, username = ?
                WHERE id = ?
                """
            
                if username:
                    encrypted_username = CryptoUtils.EncryptWithPublicKey(publicKey, username)
                else:
                    encrypted_username = None
                
                parameters = (firstName, lastName, encrypted_username,userId)

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
    
    def UpdateScooter(self, scooter_id, updates: dict, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return "FAIL"
            if not updates:
                print("No fields to update.")
                return "OK"

            validators = {
                "brand":                InputValidation.ValidateBrandOrModel,
                "model":                InputValidation.ValidateBrandOrModel,
                "serial_number":        InputValidation.ValidateSerialNumber,
                "top_speed":            lambda v: InputValidation.ValidateIntegerInRange(v, 5, 120),
                "battery_capacity":     lambda v: InputValidation.ValidateIntegerInRange(v, 100, 2000),
                "state_of_charge":      lambda v: InputValidation.ValidateIntegerInRange(v, 0, 100),
                "target_soc_min":       lambda v: InputValidation.ValidateIntegerInRange(v, 0, 100),
                "target_soc_max":       lambda v: InputValidation.ValidateIntegerInRange(v, 0, 100),
                "mileage":              lambda v: InputValidation.ValidateIntegerInRange(v, 0, 999999),
                "last_maintenance_date": Utility.ValidateBirthdate,
                "latitude":             InputValidation.ValidateLatitude,
                "longitude":            InputValidation.ValidateLongitude,
                "out_of_service":           InputValidation.ValidateStatus
            }

            allowed_fields = set(validators.keys())

            validated_updates = {k: v for k, v in updates.items() if k in allowed_fields}
            if not validated_updates:
                print("No valid fields provided.")
                return "FAIL"

            for field, value in validated_updates.items():
                validator = validators.get(field)
                if not validator:
                    return "FAIL"
                if not validator(value):
                    print(f"Validation failed for field '{field}' with value '{value}'")
                    return "FAIL"

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM scooters WHERE id = ?", (scooter_id,))
            if not cursor.fetchone():
                print("Scooter not found.")
                return "FAIL"

            public_key = CryptoUtils.LoadPublicKey()
            encrypted_updates = {}

            for key, value in validated_updates.items():
                if key in ["serial_number", "latitude", "longitude"]:
                    encrypted_updates[key] = CryptoUtils.EncryptWithPublicKey(public_key, str(value))
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

    def UpdateTraveller(self, traveller_id, updates: dict, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return "FAIL"
            if not updates:
                print("No fields to update.")
                return "OK"

            validators = {
                "first_name":     InputValidation.ValidateName,
                "last_name":      InputValidation.ValidateName,
                "birthday":       Utility.ValidateBirthdate,
                "gender":         InputValidation.ValidateGender,
                "street_name":    InputValidation.ValidateAddress,
                "house_number":   InputValidation.ValidateHousenumber,
                "city":           InputValidation.ValidateCity,
                "zip_code":       InputValidation.ValidateZipcode,
                "email":          InputValidation.ValidateEmailAddress,
                "mobile":         InputValidation.ValidateMobileNumber,
                "license_number": InputValidation.ValidateDrivingLicense,
            }

            updates = {k: v for k, v in updates.items() if k in validators}
            if not updates:
                print("No valid fields provided.")
                return "FAIL"

            for field, value in updates.items():
                if not validators[field](value):
                    print(f"Validation failed for field '{field}' with value '{value}'")
                    return "FAIL"

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM travellers WHERE customer_id = ?", (traveller_id,))
            if not cursor.fetchone():
                print("Traveller not found.")
                return "FAIL"

            public_key = CryptoUtils.LoadPublicKey()
            encrypted_updates = {}
            for key, value in updates.items():
                if key in ["first_name", "last_name", "gender", "street_name", "house_number", "city", "zip_code", "email", "mobile", "license_number"]:
                    encrypted_updates[key] = CryptoUtils.EncryptWithPublicKey(public_key, str(value))
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
    
    def UpdateSession(self, userID,sessionID, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return None
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query,(userID,))
            user = cursor.fetchone()

            if user:
                decryptedSessionID = Utility.SafeDecrypt(user[9])
                if str(sessionID) == decryptedSessionID:
                    new_session_id = Utility.GenerateSessionID()
                    encrypted_session_id = CryptoUtils.EncryptWithPublicKey(CryptoUtils.LoadPublicKey(),new_session_id)

                    # Step 3: Update session ID in DB
                    update_query = "UPDATE users SET session_id = ? WHERE id = ?"
                    cursor.execute(update_query, (encrypted_session_id, userID))
                    if cursor.rowcount == 1:
                        conn.commit()
                        return new_session_id
            return None
        except Exception as e:
            print(f"Something went wrong while verifying the account status: {e}")
            return None
        finally:
            if conn:
                conn.close()