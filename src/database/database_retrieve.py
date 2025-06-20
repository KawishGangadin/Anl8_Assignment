from cryptoUtils import cryptoUtils
from inputValidation import Validation
from utility import Utility
import sqlite3
import users
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

    def getAllScooters(self):
        conn = None
        try:
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

    def getAllRestoreCodes(self, user):
        conn = None
        try:
            if isinstance(user, users.superAdministrator):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM restore_codes"
                cursor.execute(query)
                codes = cursor.fetchall()
                cursor.close()
                return codes
            else:
                print("Only superadmin can retrieve all restore codes.")
                return "FAIL"
        except sqlite3.Error as e:
            print("An error occurred while fetching all restore codes:", e)
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

            userList = [] 

            if role is not None:
                for user in users:
                    encrypted_role = user[6]
                    decrypted_role_bytes = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), encrypted_role).decode('utf-8')
                    if decrypted_role_bytes == role.value:
                        decryptedUsername = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), user[3]).decode('utf-8')
                        decryptedRole = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), user[6]).decode('utf-8')
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
                decryptedUsername = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), user[3]).decode('utf-8')
                decryptedRole = cryptoUtils.decryptWithPrivateKey(cryptoUtils.loadPrivateKey(), user[6]).decode('utf-8')
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

    def getScooterById(self, scooter_id):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM scooters WHERE id = ?", (scooter_id,))
            return cursor.fetchone()  
        except sqlite3.Error as e:
            print(f"Error retrieving scooter by ID: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def getTravellerById(self, traveller_id):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id FROM travellers WHERE customer_id = ?", (traveller_id,))
            return cursor.fetchone()  
        except sqlite3.Error as e:
            print(f"Error retrieving scooter by ID: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def searchTraveller(self, search_term):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM travellers")
            travellers = cursor.fetchall()
            
            matching_travellers = []
            for traveller in travellers:
                try:
                    decrypted_customer_id = Utility.safe_decrypt(traveller[0])
                    decrypted_registration_date = Utility.safe_decrypt(traveller[1])
                    decrypted_first_name = Utility.safe_decrypt(traveller[2])
                    decrypted_last_name = Utility.safe_decrypt(traveller[3])
                    decrypted_birthdate = Utility.safe_decrypt(traveller[4])
                    decrypted_gender = Utility.safe_decrypt(traveller[5])
                    decrypted_street = Utility.safe_decrypt(traveller[6])
                    decrypted_house_number = Utility.safe_decrypt(traveller[7])
                    decrypted_city = Utility.safe_decrypt(traveller[8])
                    decrypted_zip = Utility.safe_decrypt(traveller[9])
                    decrypted_email = Utility.safe_decrypt(traveller[10])
                    decrypted_mobile = Utility.safe_decrypt(traveller[11])
                    decrypted_license = Utility.safe_decrypt(traveller[12])

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

    def searchScooter(self, search_term):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scooters")
            scooters = cursor.fetchall()
            
            matching_scooters = []
            for scooter in scooters:
                try:
                    decrypted_id = Utility.safe_decrypt(scooter[0])
                    decrypted_isd = Utility.safe_decrypt(scooter[1])
                    decrypted_brand = Utility.safe_decrypt(scooter[2])
                    decrypted_model = Utility.safe_decrypt(scooter[3])
                    decrypted_serial_number = Utility.safe_decrypt(scooter[4])
                    decrypted_top_speed = Utility.safe_decrypt(scooter[5])
                    decrypted_battery_capacity = Utility.safe_decrypt(scooter[6])
                    decrypted_soc = Utility.safe_decrypt(scooter[7])
                    decrypted_target_min = Utility.safe_decrypt(scooter[8])
                    decrypted_target_max = Utility.safe_decrypt(scooter[9])
                    decrypted_latitude = Utility.safe_decrypt(scooter[10])
                    decrypted_longitude = Utility.safe_decrypt(scooter[11])
                    decrypted_out_of_service = Utility.safe_decrypt(scooter[12])
                    decrypted_mileage = Utility.safe_decrypt(scooter[13])
                    decrypted_last_maintenance = Utility.safe_decrypt(scooter[14])

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

    def findTravellerID(self, traveller_id):
        conn = None
        private_key = cryptoUtils.loadPrivateKey() 
        try:
            if Validation.validateMembershipID(traveller_id):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM travellers"
                cursor.execute(query)
                members = cursor.fetchall()
                cursor.close()

                decrypted_membership_id = None

                for member in members:
                    decrypted_membership_id = cryptoUtils.decryptWithPrivateKey(private_key, member[0])  
                    if decrypted_membership_id.decode('utf-8') == traveller_id:
                        return True  

                return False  
            return False

        except sqlite3.Error as e:
            print("An error occurred while searching for membership ID:", e)
            return False
        finally:
            if conn:
                conn.close()