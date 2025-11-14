from cryptoUtils import CryptoUtils
from inputValidation import InputValidation
from utility import Utility
import sqlite3
import users
import time
from roles import roles

class DBRetrieve:

    def GetAllTravellers(self, userContext):
        conn = None
        try:
            if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                return []
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

    def GetAllScooters(self, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return []
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scooters")
            results = cursor.fetchall()
            cursor.close()
            return results
        except sqlite3.Error as e:
            print("Error retrieving scooter records:", e)
            return []
        finally:
            if conn:
                conn.close()
    
    def GetRestoreCodesByUser(self, user_id, userContext):
        conn = None
        try:
            if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                return []
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT code, backup_filename FROM restore_codes WHERE system_admin_id = ?"
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            cursor.close()

            private_key = CryptoUtils.LoadPrivateKey()

            decrypted_codes = []
            for encrypted_code, backup_filename in rows:
                try:
                    decrypted_code = CryptoUtils.DecryptWithPrivateKey(private_key, encrypted_code)
                    decrypted_codes.append((decrypted_code, backup_filename))
                except Exception as e:
                    print(f"Failed to decrypt restore code: {e}")
                    continue 

            return decrypted_codes

        except sqlite3.Error as e:
            print("An error occurred while fetching restore codes:", e)
            return []
        finally:
            if conn:
                conn.close()

    def GetAllRestoreCodes(self, user, userContext):
        conn = None
        try:
            if(self.AuthorizeAction(userContext, roles.SUPERADMIN)== False):
                print("Only superadmin can retrieve all restore codes.")
                return []
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM restore_codes"
            cursor.execute(query)
            codes = cursor.fetchall()
            cursor.close()
            return codes
        except sqlite3.Error as e:
            print("An error occurred while fetching all restore codes:", e)
            return []
        finally:
            if conn:
                conn.close()
    
    def GetOwnUserData(self, username, userContext):
        conn = None
        try:
            if (self.IsAuthorized(userContext) == False):
                return None
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
                        return user
            return None

        except sqlite3.Error as e:
            print("An error occurred while retrieving user data:", e)
            return None
        finally:
            if conn:
                conn.close()

    def GetUsernameByID(self, user_id, userContext):
        conn = None
        try:
            if(self.AuthorizeAny(userContext,[roles.ADMIN,roles.SUPERADMIN]) == False):
                return None
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
    
    def GetUsers(self, userContext ,role=None):
        conn = None
        try:
            if (role == None):
                if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                    return None
                else:
                    pass
            else:
                if(self.AuthorizeUserManagement(userContext,role) == False):
                    return None
                else:
                    pass
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            query = "SELECT * FROM users"
            cursor.execute(query)

            users = cursor.fetchall()
            cursor.close()

            userList = [] 

            if role is not None:
                for user in users:
                    encrypted_role = user[6]
                    decrypted_role_bytes = CryptoUtils.DecryptWithPrivateKey(CryptoUtils.LoadPrivateKey(), encrypted_role)
                    if decrypted_role_bytes == role.value:
                        decryptedUsername = CryptoUtils.DecryptWithPrivateKey(CryptoUtils.LoadPrivateKey(), user[3])
                        decryptedRole = CryptoUtils.DecryptWithPrivateKey(CryptoUtils.LoadPrivateKey(), user[6])
                        hiddenPassword = "********"  
                        decryptedUser = (
                            user[0], 
                            user[1],
                            user[2], 
                            decryptedUsername,  
                            hiddenPassword, 
                            user[5],  
                            decryptedRole 
                        )
                        userList.append(decryptedUser)

                return userList

            for user in users:
                decryptedUsername = CryptoUtils.DecryptWithPrivateKey(CryptoUtils.LoadPrivateKey(), user[3])
                decryptedRole = CryptoUtils.DecryptWithPrivateKey(CryptoUtils.LoadPrivateKey(), user[6])
                hiddenPassword = "********"  
                decryptedUser = (
                    user[0], 
                    user[1], 
                    user[2],  
                    decryptedUsername, 
                    hiddenPassword, 
                    user[5], 
                    decryptedRole 
                )
                userList.append(decryptedUser)

            return userList

        except sqlite3.Error as e:
            print("An error occurred while retrieving users:", e)
            return None

        finally:
            if conn:
                conn.close()
    
    def GetUserRole(self, userID):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT role FROM users WHERE id = ?"
            cursor.execute(query, (userID,))
            role = cursor.fetchone()
            cursor.close()
            if role:
                decrypted_role = CryptoUtils.DecryptWithPrivateKey(CryptoUtils.LoadPrivateKey(), role[0])
                return decrypted_role
            return None
        except sqlite3.Error as e:
            print("An error occurred while retrieving user role:", e)
            return None
        finally:
            if conn:
                conn.close()

    def DisplayAllTravellers(self, userContext):
        try:
            if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                return None
            travellers = self.GetAllTravellers(userContext)

            print("\n======= Registered Travellers =======")
            for t in travellers:
                print(f"Customer ID: {Utility.SafeDecrypt(t[0])}")
                print(f"Registration Date: {Utility.SafeDecrypt(t[1])}")
                print(f"Name: {Utility.SafeDecrypt(t[2])} {Utility.SafeDecrypt(t[3])}")
                print(f"Birthdate: {t[4]}")
                print(f"Gender: {Utility.SafeDecrypt(t[5])}")
                print(f"Street: {Utility.SafeDecrypt(t[6])} {Utility.SafeDecrypt(t[7])}")
                print(f"City: {Utility.SafeDecrypt(t[8])}")
                print(f"Zip: {Utility.SafeDecrypt(t[9])}")
                print(f"Email: {Utility.SafeDecrypt(t[10])}")
                print(f"Mobile: {Utility.SafeDecrypt(t[11])}")
                print(f"License: {Utility.SafeDecrypt(t[12])}")
                print("-------------------------------------")
        except Exception as e:
            print("An error occurred while displaying travellers:", e)

    def DisplayAllScooters(self, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return None
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scooters")
            scooters = cursor.fetchall()
            cursor.close()

            print("\n======= Registered Scooters =======")
            for s in scooters:
                print(f"ID: {s[0]}")
                print(f"In Service: {s[1]}")
                print(f"Brand: {s[2]}")
                print(f"Model: {s[3]}")
                print(f"Serial Number: {Utility.SafeDecrypt(s[4])}")
                print(f"Top Speed: {s[5]} km/h")
                print(f"Battery Capacity: {s[6]} Wh")
                print(f"SoC: {s[7]}%, Target Min: {s[8]}%, Target Max: {s[9]}%")
                print(f"Latitude: {Utility.SafeDecrypt(s[10])}")
                print(f"Longitude: {Utility.SafeDecrypt(s[11])}")
                print(f"Out of Service: {'Yes' if s[12] else 'No'}")
                print(f"Mileage: {s[13]} km")
                print(f"Last Maintenance: {s[14]}")
                print("-------------------------------------")

        except sqlite3.Error as e:
            print("An error occurred while retrieving scooters:", e)
        finally:
            if conn:
                conn.close()

    def GetScooterById(self, scooter_id, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return None
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scooters WHERE id = ?", (scooter_id,))
            row = cursor.fetchone()
            if row is None:
                return None

            cols = [desc[0] for desc in cursor.description]
            decrypted = {
                cols[i]: Utility.SafeDecrypt(val)
                for i, val in enumerate(row)
            }
            return decrypted

        except sqlite3.Error as e:
            print(f"Error retrieving scooter by ID: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def GetTravellerById(self, traveller_id, userContext):
        conn = None
        try:
            if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                return None
            if not InputValidation.ValidateMembershipID(traveller_id):
                print("Invalid traveller ID format.")
                return None
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM travellers WHERE customer_id = ?", (traveller_id,))
            row = cursor.fetchone()
            if row is None:
                return None

            cols = [desc[0] for desc in cursor.description]
            decrypted = {
                cols[i]: Utility.SafeDecrypt(val)
                for i, val in enumerate(row)
            }
            return decrypted 
        except sqlite3.Error as e:
            print(f"Error retrieving scooter by ID: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def SearchTraveller(self, search_term, userContext):
        conn = None
        try:
            if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                return None
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM travellers")
            travellers = cursor.fetchall()
            
            matching_travellers = []
            for traveller in travellers:
                try:
                    decrypted_customer_id = Utility.SafeDecrypt(traveller[0])
                    decrypted_registration_date = Utility.SafeDecrypt(traveller[1])
                    decrypted_first_name = Utility.SafeDecrypt(traveller[2])
                    decrypted_last_name = Utility.SafeDecrypt(traveller[3])
                    decrypted_birthdate = Utility.SafeDecrypt(traveller[4])
                    decrypted_gender = Utility.SafeDecrypt(traveller[5])
                    decrypted_street = Utility.SafeDecrypt(traveller[6])
                    decrypted_house_number = Utility.SafeDecrypt(traveller[7])
                    decrypted_city = Utility.SafeDecrypt(traveller[8])
                    decrypted_zip = Utility.SafeDecrypt(traveller[9])
                    decrypted_email = Utility.SafeDecrypt(traveller[10])
                    decrypted_mobile = Utility.SafeDecrypt(traveller[11])
                    decrypted_license = Utility.SafeDecrypt(traveller[12])

                    if (search_term.lower() in decrypted_customer_id.lower() or
                        search_term.lower() in decrypted_registration_date.lower() or
                        search_term.lower() in decrypted_first_name.lower() or
                        search_term.lower() in decrypted_last_name.lower() or
                        search_term.lower() in decrypted_birthdate.lower() or
                        search_term.lower() in decrypted_gender.lower() or
                        search_term.lower() in decrypted_street.lower() or
                        search_term.lower() in decrypted_house_number.lower() or
                        search_term.lower() in decrypted_city.lower() or
                        search_term.lower() in decrypted_zip.lower() or
                        search_term.lower() in decrypted_email.lower() or
                        search_term.lower() in decrypted_mobile.lower() or
                        search_term.lower() in decrypted_license.lower()):
        
                        decrypted_traveller = (
                            decrypted_customer_id,
                            decrypted_registration_date,
                            decrypted_first_name,
                            decrypted_last_name,
                            decrypted_birthdate,
                            decrypted_gender,
                            decrypted_street,
                            decrypted_house_number,
                            decrypted_city,
                            decrypted_zip,
                            decrypted_email,
                            decrypted_mobile,
                            decrypted_license
                        )
                        matching_travellers.append(decrypted_traveller)
                
                except Exception as e:
                    print(f"Error decrypting member data: {str(e)}")
            
            cursor.close()
            return matching_travellers
        
        except sqlite3.Error as e:
            print("An error occurred while searching members:", e)
            return None
        
        except Exception as e:
            print("An error occurred:", e)
            return None
        
        finally:
            if conn:
                conn.close()

    def SearchScooter(self, search_term, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return None
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scooters")
            scooters = cursor.fetchall()
            
            matching_scooters = []
            for scooter in scooters:
                try:
                    decrypted_id = Utility.SafeDecrypt(scooter[0])
                    decrypted_isd = Utility.SafeDecrypt(scooter[1])
                    decrypted_brand = Utility.SafeDecrypt(scooter[2])
                    decrypted_model = Utility.SafeDecrypt(scooter[3])
                    decrypted_serial_number = Utility.SafeDecrypt(scooter[4])
                    decrypted_top_speed = Utility.SafeDecrypt(scooter[5])
                    decrypted_battery_capacity = Utility.SafeDecrypt(scooter[6])
                    decrypted_soc = Utility.SafeDecrypt(scooter[7])
                    decrypted_target_min = Utility.SafeDecrypt(scooter[8])
                    decrypted_target_max = Utility.SafeDecrypt(scooter[9])
                    decrypted_latitude = Utility.SafeDecrypt(scooter[10])
                    decrypted_longitude = Utility.SafeDecrypt(scooter[11])
                    decrypted_out_of_service = Utility.SafeDecrypt(scooter[12])
                    decrypted_mileage = Utility.SafeDecrypt(scooter[13])
                    decrypted_last_maintenance = Utility.SafeDecrypt(scooter[14])

                    if (search_term.lower() in decrypted_id.lower() or
                        search_term.lower() in decrypted_isd.lower() or
                        search_term.lower() in decrypted_brand.lower() or
                        search_term.lower() in decrypted_model.lower() or
                        search_term.lower() in decrypted_serial_number.lower() or
                        search_term.lower() in decrypted_top_speed.lower() or
                        search_term.lower() in decrypted_battery_capacity.lower() or
                        search_term.lower() in decrypted_soc.lower() or
                        search_term.lower() in decrypted_target_min.lower() or
                        search_term.lower() in decrypted_target_max.lower() or
                        search_term.lower() in decrypted_latitude.lower() or
                        search_term.lower() in decrypted_longitude.lower() or
                        search_term.lower() in decrypted_out_of_service.lower() or
                        search_term.lower() in decrypted_mileage.lower() or
                        search_term.lower() in decrypted_last_maintenance.lower()):
        
                        decrypted_scooter = (
                            decrypted_id,
                            decrypted_isd,
                            decrypted_brand,
                            decrypted_model,
                            decrypted_serial_number,
                            decrypted_top_speed,
                            decrypted_battery_capacity,
                            decrypted_soc,
                            decrypted_target_min,
                            decrypted_target_max,
                            decrypted_latitude,
                            decrypted_longitude,
                            decrypted_out_of_service,
                            decrypted_mileage,
                            decrypted_last_maintenance
                        )
                        matching_scooters.append(decrypted_scooter)
                
                except Exception as e:
                    print(f"Error decrypting member data: {str(e)}")
            
            cursor.close()
            return matching_scooters
        
        except sqlite3.Error as e:
            print("An error occurred while searching members:", e)
            return None
        
        except Exception as e:
            print("An error occurred:", e)
            return None
        
        finally:
            if conn:
                conn.close()

    def FindTravellerID(self, traveller_id, userContext):
        conn = None
        private_key = CryptoUtils.LoadPrivateKey() 
        try:
            if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                return None
            if InputValidation.ValidateMembershipID(traveller_id):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM travellers"
                cursor.execute(query)
                members = cursor.fetchall()
                cursor.close()

                decrypted_membership_id = None

                for member in members:
                    decrypted_membership_id = CryptoUtils.DecryptWithPrivateKey(private_key, member[0])  
                    if decrypted_membership_id == traveller_id:
                        return True  

                return False  
            return False

        except sqlite3.Error as e:
            print("An error occurred while searching for membership ID:", e)
            return False
        finally:
            if conn:
                conn.close()