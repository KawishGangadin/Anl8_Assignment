from datetime import date
import sqlite3
from sqlite3 import Error
from users import roles
from cryptoUtils import cryptoUtils
import os


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
                decrypted_role = cryptoUtils.decryptWithPrivateKey(private_key, user[6])  # Assuming role is stored as encrypted bytes in user[7]
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

    
    def searchMember(self, search_key):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            
            # Fetch all members from the database
            cursor.execute("SELECT * FROM members")
            all_members = cursor.fetchall()
            
            # Initialize a list to store matching members
            matching_members = []
            
            # Decrypt and compare each member's fields
            privateKey = cryptoUtils.loadPrivateKey()
            for member in all_members:
                try:
                    # Ensure each member field is in bytes format before decryption
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
                    decrypted_registration_date = member[11]  # Assuming registration_date is not encrypted       
                    # Print decrypted values for debugging   
                    # Check if any decrypted field contains the search_key (case insensitive)
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
                        
                        # Append decrypted member details to matching_members list
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
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()

            # Decrypt and find the user
            private_key = cryptoUtils.loadPrivateKey()
            for user in users:
                decrypted_username_bytes = cryptoUtils.decryptWithPrivateKey(private_key, user[3]) 
                decrypted_username = decrypted_username_bytes.decode('utf-8')  # Assuming UTF-8 encoding
                if decrypted_username == username:
                    return user

            # If user is not found
            print(f"User with username {username} not found.")
            return None

        except sqlite3.Error as e:
            print("An error occurred while retrieving user data:", e)
            return None
        finally:
            if conn:
                conn.close()

    def findMembershipID(self, encrypted_membership_id):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM members"
            cursor.execute(query)
            members = cursor.fetchall()
            cursor.close()

            private_key = cryptoUtils.loadPrivateKey()  # Load private key for decryption
            decrypted_membership_id = None

            for member in members:
                decrypted_membership_id = cryptoUtils.decryptWithPrivateKey(private_key, member[0])  # Assuming membership_id is in the 2nd column
                if decrypted_membership_id.decode('utf-8') == encrypted_membership_id:
                    return True  # Found matching membership ID

            return False  # No matching membership ID found

        except sqlite3.Error as e:
            print("An error occurred while searching for membership ID:", e)
            return False
        finally:
            if conn:
                conn.close()

    
    def findUserID(self, user_id, role):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()

            private_key = cryptoUtils.loadPrivateKey()  # Load private key for decryption
            decrypted_role = None

            for user in users:
                decrypted_role = cryptoUtils.decryptWithPrivateKey(private_key, user[6])  # Assuming role is in the 7th column
                if decrypted_role.decode('utf-8') == role.value:
                    if user[0] == user_id:
                        return True  # Found matching user_id and role

            return False  # No matching user_id and role found

        except sqlite3.Error as e:
            print("An error occurred while searching for user ID:", e)
            return False
        finally:
            if conn:
                conn.close()

    
    def findUsername(self, username):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            
            users = cursor.fetchall()
            cursor.close()
            
            private_key = cryptoUtils.loadPrivateKey()
            
            for user in users:
                decrypted_username_bytes = cryptoUtils.decryptWithPrivateKey(private_key, user[3])
                decrypted_username = decrypted_username_bytes.decode('utf-8')  # Assuming UTF-8 encoding
                
                if decrypted_username == username:
                    return True
            
            return False
        
        except sqlite3.Error as e:
            print("An error occurred while searching for username:", e)
            return False
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
            if role is not None:
                private_key = cryptoUtils.loadPrivateKey()
                userList = []
                for user in users:
                    encrypted_role = user[6]  # Assuming role is stored as encrypted bytes in user[6]
                    decrypted_role_bytes = cryptoUtils.decryptWithPrivateKey(private_key, encrypted_role).decode('utf-8')
                    if decrypted_role_bytes == role.value:
                        userList.append(user)
                
                return userList
            
            return users
        
        except sqlite3.Error as e:
            print("An error occurred while retrieving users:", e)
            return None
        
        finally:
            if conn:
                conn.close()

    
    def getMembers(self):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM members"
            cursor.execute(query)
            members = cursor.fetchall()
            cursor.close()
            return members
        except sqlite3.Error as e:
            print("An error occurred while retrieving members:", e)
            return None
        finally:
            if conn:
                conn.close()

    def createMember(self, first_name, last_name, age, gender, weight, address, city, postalCode, email, mobile, registration_date, membership_id):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            query = """
            INSERT INTO members (membership_id, first_name, last_name, age, gender, weight, address, city, postalCode, email, mobile, registration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            parameters = (membership_id, first_name, last_name, age, gender, weight, address, city, postalCode, email, mobile, registration_date)
            cursor = conn.cursor()

            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while creating the member:", e)
            return None
        finally:
            if conn:
                conn.close()

    def createUser(self, first_name, last_name, username, password, registration_date, role, temp):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            hashed_password, salt = cryptoUtils.hashPassword(password)
            query = "INSERT INTO users (first_name, last_name, username, password_hash, registration_date, role, temp, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            parameters = (first_name, last_name, username, hashed_password, registration_date, role, temp, salt)
            cursor = conn.cursor()

            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while creating the user:", e)
            return None
        finally:
            if conn:
                conn.close()

    def deleteUser(self, user_id, role):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            
            if user is None:
                raise ValueError(f"No user found with id {user_id}")
            
            private_key = cryptoUtils.loadPrivateKey()  # Load private key for decryption
            decrypted_role = cryptoUtils.decryptWithPrivateKey(private_key, user[6])  # Assuming role is in the 7th column
            
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
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            # Fetch all members
            query = "SELECT * FROM members"
            cursor.execute(query)
            members = cursor.fetchall()

            # Decrypt and find the member
            private_key = cryptoUtils.loadPrivateKey()
            found_member = False
            for member in members:
                decrypted_membership_id = cryptoUtils.decryptWithPrivateKey(private_key, member[0])  # Assuming membership_id is in the second column
                if decrypted_membership_id.decode('utf-8') == membership_id:  # Decode bytes to string for comparison
                    query = "DELETE FROM members WHERE membership_id = ?"
                    cursor.execute(query, (member[0],))  # Pass the original encrypted membership_id to delete
                    conn.commit()
                    found_member = True
                    break

            cursor.close()

            if found_member:
                return "OK"
            else:
                print(f"No member found with membership ID {membership_id}.")
                return "NOT FOUND"

        except sqlite3.Error as e:
            print("An error occurred while deleting the member:", e)
            return "FAIL"

        finally:
            if conn:
                conn.close()


    def updateUser(self, userId, firstName, lastName, username):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            privateKey = cryptoUtils.loadPrivateKey()
            oldUsername = self.getUsernameByID(userId)
            publicKey = cryptoUtils.loadPublicKey()
            cursor = conn.cursor()
            query = """
            UPDATE users
            SET first_name = ?, last_name = ?, username = ?
            WHERE id = ? AND username = ?
            """
            
            # Encrypt username if needed
            if username:
                encrypted_username = cryptoUtils.encryptWithPublicKey(publicKey, username)
            else:
                encrypted_username = None
            
            parameters = (firstName, lastName, encrypted_username, userId, oldUsername)

            print("Executing query:")
            print(query)
            print("Parameters:")
            print(parameters)

            cursor.execute(query, parameters)
            
            if cursor.rowcount > 0:
                result = "OK"
            else:
                result = "No rows updated"
        
            conn.commit()  # Commit the transaction
            
            cursor.close()
            return result

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
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            publicKey = cryptoUtils.loadPublicKey()
            privateKey = cryptoUtils.loadPrivateKey()
            # Retrieve and decrypt all member records
            cursor.execute("SELECT * FROM members")
            members = cursor.fetchall()
            member_found = False

            for member in members:
                member_dict = {description[0]: member[idx] for idx, description in enumerate(cursor.description)}
                
                # Decrypt membership_id
                decrypted_membership_id_bytes = cryptoUtils.decryptWithPrivateKey(privateKey,member_dict['membership_id'])
                decrypted_membership_id = decrypted_membership_id_bytes.decode()  # Assuming membership_id needs to be decoded as string
                
                if decrypted_membership_id == membershipID:
                    member_found = True
                    # Encrypt fields to be updated
                    encrypted_fields = {key: cryptoUtils.encryptWithPublicKey(publicKey, str(value)) for key, value in fields.items()}  # Ensure value is encoded properly
                    
                    # Build the update query
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

        except sqlite3.Error as e:
            print("An error occurred while updating the member:", e)
            return None

        finally:
            if conn:
                conn.close()

    def updatePassword(self, userId, newPassword, temp=False):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()

            # Hash the new password with a new salt
            hashed_password, salt = cryptoUtils.hashPassword(newPassword)

            temp_flag = 1 if temp else 0
            query = "UPDATE users SET password_hash = ?, temp = ?, salt = ? WHERE id = ?"
            parameters = (hashed_password, temp_flag, salt, userId)

            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while updating the password:", e)
            return None
        finally:
            if conn:
                conn.close()

    def getUsernameByID(self, user_id):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT username FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            username = cursor.fetchone()
            cursor.close()
            return username[0] if username else None
        except sqlite3.Error as e:
            print("An error occurred while retrieving username by user ID:", e)
            return None
        finally:
            if conn:
                conn.close()