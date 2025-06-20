from cryptoUtils import cryptoUtils
from inputValidation import Validation
from roles import roles
import sqlite3
import secrets
import string
import os
class DBCreate:

    def createTravellersTable(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS travellers (
            customer_id TEXT PRIMARY KEY,
            registration_date TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            birthday TEXT NOT NULL,
            gender TEXT NOT NULL,
            street_name TEXT NOT NULL,
            house_number INTEGER NOT NULL,
            city TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            email TEXT,
            mobile TEXT NOT NULL,
            license_number TEXT NOT NULL
        )
        """
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute(create_query)
            conn.commit()
        except sqlite3.Error as e:
            print("An error occurred while creating the travellers table:", e)
        finally:
            if conn:
                conn.close()

    def createScootersTable(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS scooters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            in_service_date TEXT NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            serial_number TEXT NOT NULL,
            top_speed INTEGER NOT NULL,
            battery_capacity INTEGER NOT NULL,
            state_of_charge INTEGER NOT NULL,
            target_soc_min INTEGER NOT NULL,    
            target_soc_max INTEGER NOT NULL,
            latitude REAL NOT NULL, 
            longitude REAL NOT NULL, 
            out_of_service BOOLEAN NOT NULL DEFAULT 0,
            mileage INTEGER NOT NULL,
            last_maintenance_date TEXT NOT NULL
        )
        """
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute(create_query)
            conn.commit()
        except sqlite3.Error as e:
            print("An error occurred while creating the travellers table:", e)
        finally:
            if conn:
                conn.close()

    def createBackupsTable(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS restore_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system_admin_id INTEGER NOT NULL,
            code TEXT NOT NULL UNIQUE,
            backup_filename TEXT NOT NULL,
            used BOOLEAN NOT NULL DEFAULT 0
        )        
        """
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute(create_query)
            conn.commit()
        except sqlite3.Error as e:
            print("An error occurred while creating the backups table:", e)
        finally:
            if conn:
                conn.close()

    def createUsersTable(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            registration_date DATE NOT NULL,
            role TEXT NOT NULL,
            temp BOOLEAN NOT NULL,
            salt TEXT NOT NULL,
            session_id INTEGER NOT NULL DEFAULT 0
        )
        """
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute(create_query)
            conn.commit()
        except sqlite3.Error as e:
            print("An error occurred while creating the users table:", e)
        finally:
            if conn:
                conn.close()
    
    def createTraveller(self, customer_id, registration_date, first_name, last_name, birthdate,
                    gender, street, house_number, city, zip_code, email, mobile, license_number):
        conn = None
        try:
            # Defensive validation
            if not (Validation.validateName(first_name)
                    and Validation.validateName(last_name)
                    and Validation.validateHousenumber(str(house_number))
                    and Validation.validateZipcode(zip_code)
                    and Validation.validateCity(city)
                    and Validation.validateEmail(email)
                    and Validation.validateMobileNumber(mobile)):
                print("Validation failed during backend traveller creation.")
                return "FAIL"

            public_key = cryptoUtils.loadPublicKey()

            encrypted_first_name = cryptoUtils.encryptWithPublicKey(public_key, first_name)
            encrypted_last_name = cryptoUtils.encryptWithPublicKey(public_key, last_name)
            encrypted_house_number = cryptoUtils.encryptWithPublicKey(public_key, str(house_number))
            encrypted_street_name = cryptoUtils.encryptWithPublicKey(public_key, str(street))
            encrypted_license_number = cryptoUtils.encryptWithPublicKey(public_key, str(license_number))
            encrypted_zip = cryptoUtils.encryptWithPublicKey(public_key, zip_code)
            encrypted_city = cryptoUtils.encryptWithPublicKey(public_key, city)
            encrypted_email = cryptoUtils.encryptWithPublicKey(public_key, email)
            encrypted_mobile = cryptoUtils.encryptWithPublicKey(public_key, mobile)

            # Open connection and insert
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            query = """
                INSERT INTO travellers (
                    customer_id, registration_date, first_name, last_name, birthday,
                    gender, street_name, house_number, city, zip_code, email, mobile, license_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                customer_id,
                registration_date,
                encrypted_first_name,
                encrypted_last_name,
                birthdate,
                gender,
                encrypted_street_name,
                encrypted_house_number,
                encrypted_city,
                encrypted_zip,
                encrypted_email,
                encrypted_mobile,
                encrypted_license_number
            ))
            conn.commit()
            cursor.close()
            return "OK"

        except sqlite3.Error as e:
            print("Database error while creating traveller:", e)
            return "FAIL"
        except Exception as e:
            print("Unexpected error while creating traveller:", e)
            return "FAIL"
        finally:
            if conn:
                conn.close()

    def createScooter(self, scooter_data):
        conn = None
        try:
            in_service_date = scooter_data.get('in_service_date')
            brand = scooter_data.get('brand')
            model = scooter_data.get('model')
            serial_number = scooter_data.get('serial_number')
            top_speed = scooter_data.get('top_speed')
            battery_capacity = scooter_data.get('battery_capacity')
            state_of_charge = scooter_data.get('state_of_charge')
            target_soc_min = scooter_data.get('target_soc_min')
            target_soc_max = scooter_data.get('target_soc_max')
            latitude = scooter_data.get('latitude')
            longitude = scooter_data.get('longitude')
            mileage = scooter_data.get('mileage')
            last_maintenance_date = scooter_data.get('last_maintenance_date')

            # Validate fields
            if not (Validation.validateBrandOrModel(brand, None) and
                    Validation.validateBrandOrModel(model, None) and
                    Validation.validateSerialNumber(serial_number) and
                    Validation.validateIntegerInRange(top_speed, 5, 120) and
                    Validation.validateIntegerInRange(battery_capacity, 100, 2000) and
                    Validation.validateIntegerInRange(state_of_charge, 0, 100) and
                    Validation.validateIntegerInRange(target_soc_min, 0, 100) and
                    Validation.validateIntegerInRange(target_soc_max, 0, 100) and
                    Validation.validateIntegerInRange(mileage, 0, 999999) and
                    Validation.validateCoordinates(latitude, longitude)):
                print("Validation failed.")
                return "FAIL"

            public_key = cryptoUtils.loadPublicKey()

            encrypted_serial = cryptoUtils.encryptWithPublicKey(public_key, serial_number)
            encrypted_lat = cryptoUtils.encryptWithPublicKey(public_key, latitude)
            encrypted_lon = cryptoUtils.encryptWithPublicKey(public_key, longitude)

            query = """
            INSERT INTO scooters (
                in_service_date, brand, model, serial_number, top_speed,
                battery_capacity, state_of_charge, target_soc_min, target_soc_max,
                latitude, longitude, out_of_service, mileage, last_maintenance_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            parameters = (
                in_service_date, brand, model, encrypted_serial,
                int(top_speed), int(battery_capacity), int(state_of_charge),
                int(target_soc_min), int(target_soc_max),
                encrypted_lat, encrypted_lon,
                0,  # Default for out_of_service
                int(mileage),
                last_maintenance_date
            )

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            return "OK"

        except sqlite3.Error as e:
            print("DB error while creating scooter:", e)
            return "FAIL"
        finally:
            if conn:
                conn.close()



    def createUser(self, first_name, last_name, username, password, registration_date, role, temp):
        conn = None
        try:
            public_key = cryptoUtils.loadPublicKey()
            validationData = { "first_name": first_name, "last_name": last_name, "username": username, "password": password }
            if Validation.validateMultipleInputs( **validationData) and role in [roles.ADMIN, roles.SERVICE] and temp in [False,True] :
                conn = sqlite3.connect(self.databaseFile)
                hashed_password, salt = cryptoUtils.hashPassword(password)
                encryptedRole = cryptoUtils.encryptWithPublicKey(public_key,role.value)
                encryptedUsername = cryptoUtils.encryptWithPublicKey(public_key,username.lower())
                query = "INSERT INTO users (first_name, last_name, username, password_hash, registration_date, role, temp, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                parameters = (first_name, last_name, encryptedUsername, hashed_password, registration_date, encryptedRole, temp, salt)
                cursor = conn.cursor()

                cursor.execute(query, parameters)
                conn.commit()
                cursor.close()
                return "OK"
            else:
                return "FAIL"
        except sqlite3.Error as e:
            print("An error occurred while creating the user:", e)
            return None
        finally:
            if conn:
                conn.close()

    def createRestoreCode(self, user_id, backup_name,backupSys, required_role=roles.ADMIN):
        if not self.findUserID(user_id, required_role):
            print("User ID is invalid or does not have the required role.")
            return "FAIL"

        if not backupSys.doesBackupExist(backup_name):
            print("Backup file does not exist.")
            return "FAIL"

        def generate_code(length=16):
            chars = string.ascii_letters + string.digits
            return ''.join(secrets.choice(chars) for _ in range(length))

        restore_code = generate_code()

        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = """
                INSERT INTO restore_codes (system_admin_id, code, backup_filename)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (user_id, restore_code, backup_name))
            conn.commit()
            cursor.close()
            print(f"Restore code created: {restore_code}")
            return restore_code  
        except sqlite3.Error as e:
            print("An error occurred while inserting the restore code:", e)
            return "FAIL"
        finally:
            if conn:
                conn.close()

    

