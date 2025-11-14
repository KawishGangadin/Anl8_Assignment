import sys
from cryptoUtils import CryptoUtils
from utility import Utility
from inputValidation import InputValidation
import sqlite3
from roles import roles

class DBUpdate:
    
    def UpdatePassword(self, userId, newPassword, userContext, role,temp=False):
        conn = None
        try:
            if(self.AuthorizeUserManagement(userContext,role) == False):
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

    def UpdateOwnPassword(self, userId, newPassword, userContext, temp=False):
        conn = None
        try:
            if(userId == userContext.id and self.AuthorizeAny(userContext,[roles.ADMIN,roles.SERVICE]) == False):
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

    def UpdateUser(self, userId, firstName, lastName, username, userContext,role):
        conn = None
        try:
            if (self.AuthorizeUserManagement(userContext, role)):
                pass
            else:
                print("You are not authorized to reset passwords for other users.")
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

    def UpdateSelf(self, userId, firstName, lastName, username, userContext):
        conn = None
        try:
            if(userId == userContext.id and self.IsAuthorized(userContext) == False):
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
                "top_speed":            lambda v: Utility.ValidateIntegerInRange(v, "5", "120"),
                "battery_capacity":     lambda v: Utility.ValidateIntegerInRange(v, "100", "2000"),
                "state_of_charge":      lambda v: Utility.ValidateIntegerInRange(v, "0", "100"),
                "target_soc_min":       lambda v: Utility.ValidateIntegerInRange(v, "0", "100"),
                "target_soc_max":       lambda v: Utility.ValidateIntegerInRange(v, "0", "100"),
                "mileage":              lambda v: Utility.ValidateIntegerInRange(v, "0", "999999"),
                "last_maintenance_date": Utility.ValidateDate,
                "latitude":             Utility.ValidateLatitude,
                "longitude":            Utility.ValidateLongtitude,
                "out_of_service":           InputValidation.ValidateStatus
            }
            
            allowed_fields = set(validators.keys())
            if userContext.role == roles.SERVICE:
                allowed_fields = {
                    "state_of_charge",
                    "target_soc_min",
                    "target_soc_max",
                    "mileage",
                    "last_maintenance_date",
                    "out_of_service"
                }
            else:
                allowed_fields = set(validators.keys())
            disallowed = [k for k in updates.keys() if k not in allowed_fields]
            if disallowed:
                print(f"These fields are not allowed for your role: {', '.join(disallowed)}")
                return "FAIL"

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
            if(self.AuthorizeTavellerManagement(userContext) == False):
                return "FAIL"
            if not updates:
                print("No fields to update.")
                return "OK"

            validators = {
                "first_name":     InputValidation.ValidateName,
                "last_name":      InputValidation.ValidateName,
                "birthday":       Utility.ValidateDate,
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
                print("Unauthorized access detected. Exiting.")
                sys.exit()
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