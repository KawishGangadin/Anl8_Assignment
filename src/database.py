from datetime import date
import sqlite3
from sqlite3 import Error
from roles import roles
from cryptoUtils import cryptoUtils
from inputValidation import Validation
import os
import time


class DB:
    def __init__(self, databaseFile) -> None:
        self.databaseFile = databaseFile

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
            salt TEXT NOT NULL
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

    def findMembershipID(self, membership_id):
        conn = None
        private_key = cryptoUtils.loadPrivateKey() 
        try:
            if Validation.validateMembershipID(membership_id):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM members"
                cursor.execute(query)
                members = cursor.fetchall()
                cursor.close()

                decrypted_membership_id = None

                for member in members:
                    decrypted_membership_id = cryptoUtils.decryptWithPrivateKey(private_key, member[0])  
                    if decrypted_membership_id.decode('utf-8') == membership_id:
                        return True  

                return False  
            return False

        except sqlite3.Error as e:
            print("An error occurred while searching for membership ID:", e)
            return False
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

    def searchMember(self, search_key):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members")
            all_members = cursor.fetchall()
            
            matching_members = []
            privateKey = cryptoUtils.loadPrivateKey()
            for member in all_members:
                try:
                    decrypted_membership_id = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[0])).decode('utf-8')
                    decrypted_first_name = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[1])).decode('utf-8')
                    decrypted_last_name = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[2])).decode('utf-8')
                    decrypted_age = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[3])).decode('utf-8')
                    decrypted_gender = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[4])).decode('utf-8')
                    decrypted_weight = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[5])).decode('utf-8')
                    decrypted_address = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[6])).decode('utf-8')
                    decrypted_city = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[7])).decode('utf-8')
                    decrypted_postal_code = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[8])).decode('utf-8')
                    decrypted_email = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[9])).decode('utf-8')
                    decrypted_mobile = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[10])).decode('utf-8')
                    decrypted_registration_date = member[11] 

                    if (search_key.lower() in decrypted_membership_id.lower() or
                        search_key.lower() in decrypted_first_name.lower() or
                        search_key.lower() in decrypted_last_name.lower() or
                        search_key.lower() in decrypted_age.lower() or
                        search_key.lower() in decrypted_gender.lower() or
                        search_key.lower() in decrypted_weight.lower() or
                        search_key.lower() in decrypted_address.lower() or
                        search_key.lower() in decrypted_city.lower() or
                        search_key.lower() in decrypted_postal_code.lower() or
                        search_key.lower() in decrypted_email.lower() or
                        search_key.lower() in decrypted_mobile.lower()):
        
                        decrypted_member = (
                            decrypted_membership_id,
                            decrypted_first_name,
                            decrypted_last_name,
                            decrypted_age,
                            decrypted_gender,
                            decrypted_weight,
                            decrypted_address,
                            decrypted_city,
                            decrypted_postal_code,
                            decrypted_email,
                            decrypted_mobile,
                            decrypted_registration_date,
                        )
                        matching_members.append(decrypted_member)
                
                except Exception as e:
                    print(f"Error decrypting member data: {str(e)}")
            
            cursor.close()
            return matching_members
        
        except sqlite3.Error as e:
            print("An error occurred while searching members:", e)
            return None
        
        except Exception as e:
            print("An error occurred:", e)
            return None
        
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
                decrypted_membership_id = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[0])).decode('utf-8')
                decrypted_first_name = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[1])).decode('utf-8')
                decrypted_last_name = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[2])).decode('utf-8')
                decrypted_age = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[3])).decode('utf-8')
                decrypted_gender = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[4])).decode('utf-8')
                decrypted_weight = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[5])).decode('utf-8')
                decrypted_address = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[6])).decode('utf-8')
                decrypted_city = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[7])).decode('utf-8')
                decrypted_postal_code = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[8])).decode('utf-8')
                decrypted_email = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[9])).decode('utf-8')
                decrypted_mobile = cryptoUtils.decryptWithPrivateKey(privateKey, bytes(member[10])).decode('utf-8')
                decrypted_registration_date = member[11] 
                decrypted_member = (
                            decrypted_membership_id,
                            decrypted_first_name,
                            decrypted_last_name,
                            decrypted_age,
                            decrypted_gender,
                            decrypted_weight,
                            decrypted_address,
                            decrypted_city,
                            decrypted_postal_code,
                            decrypted_email,
                            decrypted_mobile,
                            decrypted_registration_date,
                        )
                memberList.append(decrypted_member)
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

    def updateMember(self, membershipID, **fields):
        conn = None

        try:
            if(len(fields) == 0):
                return "OK"
            if Validation.validateMultipleInputs(**fields):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                publicKey = cryptoUtils.loadPublicKey()
                privateKey = cryptoUtils.loadPrivateKey()
                cursor.execute("SELECT * FROM members")
                members = cursor.fetchall()
                member_found = False

                for member in members:
                    member_dict = {description[0]: member[idx] for idx, description in enumerate(cursor.description)}
                    decrypted_membership_id_bytes = cryptoUtils.decryptWithPrivateKey(privateKey,member_dict['membership_id'])
                    decrypted_membership_id = decrypted_membership_id_bytes.decode()  
                    
                    if decrypted_membership_id == membershipID:
                        member_found = True
                        encrypted_fields = {key: cryptoUtils.encryptWithPublicKey(publicKey, str(value)) for key, value in fields.items()}  
                        
                        query = "UPDATE members SET"
                        parameters = []
                        
                        for field, value in encrypted_fields.items():
                            query += f" {field} = ?,"
                            parameters.append(value)
                        
                        query = query.rstrip(",") + " WHERE membership_id = ?"
                        parameters.append(member_dict['membership_id'])
                        
                        cursor.execute(query, parameters)
                        conn.commit()
                        break
                
                cursor.close()
                return "OK" if member_found else "Member not found"
            else:
                return "FAIL"

        except sqlite3.Error as e:
            print("An error occurred while updating the member:", e)
            return None

        finally:
            if conn:
                conn.close()

    def updatePassword(self, userId, newPassword, temp=False):
        conn = None
        try:
            if Validation.passwordValidation(newPassword):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()

                hashed_password, salt = cryptoUtils.hashPassword(newPassword)

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

    def deleteUser(self, user_id, role):
        conn = None
        try:
            if str(user_id).isdigit() and role.value in [roles.ADMIN.value, roles.CONSULTANT.value]:
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM users WHERE id = ?"
                cursor.execute(query, (user_id,))
                user = cursor.fetchone()
                
                if user is None:
                    raise ValueError(f"No user found with id {user_id}")
                
                private_key = cryptoUtils.loadPrivateKey() 
                decrypted_role = cryptoUtils.decryptWithPrivateKey(private_key, user[6])  
                
                if decrypted_role.decode('utf-8') == role.value:
                    delete_query = "DELETE FROM users WHERE id = ? AND role = ?"
                    cursor.execute(delete_query, (user_id, user[6]))
                    conn.commit()
                    
                    if cursor.rowcount == 0:
                        raise ValueError(f"No user found with id {user_id} and role {role.value}")
                    
                    cursor.close()
                    return "OK"
                else:
                    raise ValueError(f"Role mismatch for user with id {user_id}")
            return "FAIL"
        
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the user: {e}")
            return "FAIL"
        except ValueError as ve:
            print(str(ve))
            return "FAIL"
        finally:
            if conn:
                conn.close()

    def deleteMember(self, membership_id):
        conn = None
        try:
            if Validation.validateMembershipID(membership_id):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM members"
                cursor.execute(query)
                members = cursor.fetchall()

                private_key = cryptoUtils.loadPrivateKey()
                found_member = False
                for member in members:
                    decrypted_membership_id = cryptoUtils.decryptWithPrivateKey(private_key, member[0])  
                    if decrypted_membership_id.decode('utf-8') == membership_id: 
                        query = "DELETE FROM members WHERE membership_id = ?"
                        cursor.execute(query, (member[0],))  
                        conn.commit()
                        found_member = True
                        break

                cursor.close()

                if found_member:
                    return "OK"
                else:
                    print(f"No member found with membership ID {membership_id}.")
                    return "NOT FOUND"
            return "FAIL"

        except sqlite3.Error as e:
            print("An error occurred while deleting the member:", e)
            return "FAIL"

        finally:
            if conn:
                conn.close()
