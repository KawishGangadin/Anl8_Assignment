from cryptoUtils import cryptoUtils
from inputValidation import Validation
from roles import roles
import sqlite3
import secrets
import string
import os
class DBCreate:

    def createMembersTable(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS members (
            membership_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER CHECK(age >= 0),
            gender TEXT NOT NULL,
            weight REAL CHECK(weight >= 0),
            address TEXT NOT NULL,
            city TEXT,
            postalCode TEXT,
            email TEXT,
            mobile TEXT,
            registration_date DATE NOT NULL
        )
        """
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute(create_query)
            conn.commit()
        except sqlite3.Error as e:
            print("An error occurred while creating the members table:", e)
        finally:
            if conn:
                conn.close()

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


    def createMember(self, first_name, last_name, age, gender, weight, address, city, postalCode, email, mobile, registration_date, membership_id):
        conn = None
        try:
            validationData = { "first_name": first_name, "last_name": last_name, "age": age, "address": address, "city": city, "postalCode": postalCode, "email": email, "mobile": mobile, "membershipID": membership_id }
            if Validation.validateMultipleInputs( **validationData):
                conn = sqlite3.connect(self.databaseFile)
                query = """
                INSERT INTO members (membership_id, first_name, last_name, age, gender, weight, address, city, postalCode, email, mobile, registration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                public_key = cryptoUtils.loadPublicKey()
                encrypted_firstName = cryptoUtils.encryptWithPublicKey(public_key, first_name)
                encrypted_lastName = cryptoUtils.encryptWithPublicKey(public_key, last_name)
                encrypted_age = cryptoUtils.encryptWithPublicKey(public_key, age)
                encrypted_gender = cryptoUtils.encryptWithPublicKey(public_key, gender)
                encrypted_weight = cryptoUtils.encryptWithPublicKey(public_key, str(weight))
                encrypted_membershipId = cryptoUtils.encryptWithPublicKey(public_key, membership_id)
                encrypted_address = cryptoUtils.encryptWithPublicKey(public_key, address)
                encrypted_city = cryptoUtils.encryptWithPublicKey(public_key, city)
                encrypted_postalCode = cryptoUtils.encryptWithPublicKey(public_key, postalCode)
                encrypted_email = cryptoUtils.encryptWithPublicKey(public_key, email)
                encrypted_mobile = cryptoUtils.encryptWithPublicKey(public_key, str("316"+mobile))
                parameters = (encrypted_membershipId, encrypted_firstName, encrypted_lastName, encrypted_age, encrypted_gender, encrypted_weight, encrypted_address, encrypted_city, encrypted_postalCode, encrypted_email, encrypted_mobile, registration_date)
                cursor = conn.cursor()

                cursor.execute(query, parameters)
                conn.commit()
                cursor.close()
                return "OK"
            else:
                return "FAIL"
        except sqlite3.Error as e:
            print("An error occurred while creating the member:", e)
            return None
        finally:
            if conn:
                conn.close()

    def createUser(self, first_name, last_name, username, password, registration_date, role, temp):
        conn = None
        try:
            public_key = cryptoUtils.loadPublicKey()
            validationData = { "first_name": first_name, "last_name": last_name, "username": username, "password": password }
            if Validation.validateMultipleInputs( **validationData) and role in [roles.ADMIN, roles.CONSULTANT] and temp in [False,True] :
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

    def createRestoreCode(self, user_id, backup_name, required_role=roles.ADMIN):
        if not self.findUserID(user_id, required_role):
            print("User ID is invalid or does not have the required role.")
            return "FAIL"

        backup_path = os.path.join("backups", backup_name)
        if not os.path.isfile(backup_path):
            print("Backup file does not exist.")
            return "FAIL"

        def generate_code(length=16):
            chars = string.ascii_letters + string.digits
            return ''.join(secrets.choice(chars) for _ in range(length))

        restore_code = generate_code()

        # 4. Store the code in the restore_codes table
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
            return restore_code  # Return the code so you can display or copy it
        except sqlite3.Error as e:
            print("An error occurred while inserting the restore code:", e)
            return "FAIL"
        finally:
            if conn:
                conn.close()

    

