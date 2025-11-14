from cryptoUtils import CryptoUtils
from inputValidation import InputValidation
from roles import roles
import sqlite3
import secrets
import string

from utility import Utility

class DBCreate:

    def CreateTravellersTable(self):
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

    def CreateScootersTable(self):
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

    def CreateBackupsTable(self):
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

    def CreateUsersTable(self):
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
            session_id TEXT
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
    
    def CreateTraveller(self, traveller_data, userContext):
        conn = None
        try:
            if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                return "FAIL"
            if not (
                InputValidation.ValidateName(traveller_data["first_name"]) and
                InputValidation.ValidateName(traveller_data["last_name"]) and
                Utility.ValidateBirthdate(traveller_data["birthdate"]) and
                InputValidation.ValidateGender(traveller_data["gender"]) and
                InputValidation.ValidateAddress(traveller_data["street"]) and
                InputValidation.ValidateHousenumber(str(traveller_data["house_number"])) and
                InputValidation.ValidateCity(traveller_data["city"]) and
                InputValidation.ValidateZipcode(traveller_data["zip_code"]) and
                InputValidation.ValidateEmailAddress(traveller_data["email"]) and
                InputValidation.ValidateMobileNumber(traveller_data["mobile"]) and
                InputValidation.ValidateDrivingLicense(traveller_data["license_number"])
            ):
                print("Validation failed at database level.")
                return "FAIL"

            public_key = CryptoUtils.LoadPublicKey()

            encrypted_first_name = CryptoUtils.EncryptWithPublicKey(public_key, traveller_data["first_name"])
            encrypted_last_name = CryptoUtils.EncryptWithPublicKey(public_key, traveller_data["last_name"])
            encrypted_house_number = CryptoUtils.EncryptWithPublicKey(public_key, str(traveller_data["house_number"]))
            encrypted_street_name = CryptoUtils.EncryptWithPublicKey(public_key, traveller_data["street"])
            encrypted_city = CryptoUtils.EncryptWithPublicKey(public_key, traveller_data["city"])
            encrypted_zip = CryptoUtils.EncryptWithPublicKey(public_key, traveller_data["zip_code"])
            encrypted_email = CryptoUtils.EncryptWithPublicKey(public_key, traveller_data["email"])
            encrypted_mobile = CryptoUtils.EncryptWithPublicKey(public_key, traveller_data["mobile"])
            encrypted_license = CryptoUtils.EncryptWithPublicKey(public_key, traveller_data["license_number"])

            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            query = """
                INSERT INTO travellers (
                    customer_id, registration_date, first_name, last_name, birthday,
                    gender, street_name, house_number, city, zip_code, email, mobile, license_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(query, (
                traveller_data["customer_id"],
                traveller_data["registration_date"],
                encrypted_first_name,
                encrypted_last_name,
                traveller_data["birthdate"],
                traveller_data["gender"],
                encrypted_street_name,
                encrypted_house_number,
                encrypted_city,
                encrypted_zip,
                encrypted_email,
                encrypted_mobile,
                encrypted_license
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

    def CreateScooter(self, scooter_data, userContext):
        conn = None
        try:
            if(self.AuthorizeAny(userContext,[roles.SUPERADMIN,roles.ADMIN]) == False):
                return "FAIL"
            in_service_date = scooter_data['in_service_date']
            brand = scooter_data['brand']
            model = scooter_data['model']
            serial_number = scooter_data['serial_number']
            top_speed = scooter_data['top_speed']
            battery_capacity = scooter_data['battery_capacity']
            state_of_charge = scooter_data['state_of_charge']
            target_soc_min = scooter_data['target_soc_min']
            target_soc_max = scooter_data['target_soc_max']
            latitude = scooter_data['latitude']
            longitude = scooter_data['longitude']
            mileage = scooter_data['mileage']
            last_maintenance_date = scooter_data['last_maintenance_date']

            if not (InputValidation.ValidateBrandOrModel(brand) and 
                    InputValidation.ValidateBrandOrModel(model) and
                    InputValidation.ValidateSerialNumber(serial_number) and
                    InputValidation.ValidateSpeed(top_speed) and
                    Utility.ValidateIntegerInRange(battery_capacity, "100", "2000") and
                    Utility.ValidateIntegerInRange(state_of_charge, "0", "100") and
                    Utility.ValidateIntegerInRange(target_soc_min, "0", "100") and
                    Utility.ValidateIntegerInRange(target_soc_max, "0", "100") and
                    Utility.ValidateIntegerInRange(mileage, "0", "999999") and
                    Utility.ValidateLatitude(latitude) and
                    Utility.ValidateLongtitude(longitude)):
                print("Validation failed.")
                return "FAIL"

            public_key = CryptoUtils.LoadPublicKey()

            encrypted_serial = CryptoUtils.EncryptWithPublicKey(public_key, serial_number)
            encrypted_lat = CryptoUtils.EncryptWithPublicKey(public_key, latitude)
            encrypted_lon = CryptoUtils.EncryptWithPublicKey(public_key, longitude)

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
                0,
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

    def CreateUser(self, first_name, last_name, username, password, registration_date, role, temp, userContext):
        conn = None
        try:
            if(self.AuthorizeUserManagement(userContext,role) == False):
                return "FAIL"
            public_key = CryptoUtils.LoadPublicKey()
            validationData = { "first_name": first_name, "last_name": last_name, "username": username, "password": password }
            if InputValidation.ValidateUserInformation( **validationData) and role in [roles.ADMIN, roles.SERVICE] and temp in [False,True] :
                conn = sqlite3.connect(self.databaseFile)
                hashed_password, salt = CryptoUtils.HashPassword(password)
                encryptedRole = CryptoUtils.EncryptWithPublicKey(public_key,role.value)
                encryptedUsername = CryptoUtils.EncryptWithPublicKey(public_key,username.lower())
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

    def CreateRestoreCode(self, user_id, backup_name,backupSys,userContext,required_role=roles.ADMIN):
        if(self.AuthorizeAction(userContext,roles.SUPERADMIN) == False):
                return "FAIL"
        if not self.FindUserID(user_id, required_role):
            print("User ID is invalid or does not have the required role.")
            return "FAIL"

        if not backupSys.DoesBackupExist(backup_name):
            print("Backup file does not exist.")
            return "FAIL"

        def GenerateCode(length=16):
            chars = string.ascii_letters + string.digits
            return ''.join(secrets.choice(chars) for _ in range(length))

        restore_code = GenerateCode()
        public_key = CryptoUtils.LoadPublicKey()
        encrypted_code = CryptoUtils.EncryptWithPublicKey(public_key, restore_code)
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = """
                INSERT INTO restore_codes (system_admin_id, code, backup_filename)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (user_id, encrypted_code, backup_name))
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