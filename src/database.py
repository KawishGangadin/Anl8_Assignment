from datetime import date
import sqlite3
from sqlite3 import Error
from users import roles
from cryptoUtils import cryptoUtils


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
            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
            weight REAL CHECK(weight >= 0),
            address TEXT,
            city TEXT CHECK(city IN ('Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 'Breda', 'Nijmegen')),
            postalCode TEXT,
            email TEXT UNIQUE NOT NULL,
            mobile TEXT UNIQUE NOT NULL,
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
            password TEXT NOT NULL,
            registration_date DATE NOT NULL,
            role TEXT CHECK(role IN ('admin', 'consultant', 'superadmin')) NOT NULL,
            temp BOOLEAN NOT NULL CHECK(temp IN (0, 1)),
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

            cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'super_admin'")
            user_exists = cursor.fetchone()[0] > 0

            if not user_exists:
                hashed_password, salt = cryptoUtils.hashPassword("Admin_123?")
                
                query = """
                INSERT INTO users (first_name, last_name, username, password, registration_date, role, temp,salt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                registration_date = date.today().strftime("%Y-%m-%d")
                parameters = ("Kawish", "Gangadin", "super_admin", hashed_password, registration_date, "superadmin", 0, salt)

                cursor.execute(query, parameters)
                conn.commit()
                print("Superadmin initialized successfully.")
            else:
                print("Superadmin already exists.")

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
            query = """
            SELECT * FROM members 
            WHERE 
                membership_id LIKE ? OR
                first_name LIKE ? OR
                last_name LIKE ? OR
                address LIKE ? OR
                email LIKE ? OR
                mobile LIKE ?
            """
            search_pattern = '%' + search_key + '%'
            parameters = (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)
            
            cursor.execute(query, parameters)
            members = cursor.fetchall()
            cursor.close()
            return members
        except sqlite3.Error as e:
            print("An error occurred while searching members:", e)
            return None
        finally:
            if conn:
                conn.close()

    def getUserData(self, username):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except sqlite3.Error as e:
            print("An error occurred while retrieving user data:", e)
            return None
        finally:
            if conn:
                conn.close()

    def findMembershipID(self, membership_id):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "SELECT * FROM members WHERE membership_id = ?"
            cursor.execute(query, (membership_id,))
            
            member = cursor.fetchone()
            cursor.close()
            return member is not None
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
            query = "SELECT * FROM users WHERE role = ?"
            cursor.execute(query, (role.value,))
            
            users = cursor.fetchall()
            cursor.close()
            return any(user[0] == user_id for user in users)
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
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            
            user = cursor.fetchone()
            cursor.close()
            return user is not None
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
            
            if role is None:
                query = "SELECT * FROM users WHERE role != 'superadmin'"
                cursor.execute(query)
            else:
                query = "SELECT * FROM users WHERE role = ?"
                cursor.execute(query, (role.value,))
            
            users = cursor.fetchall()
            cursor.close()
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
            query = "INSERT INTO users (first_name, last_name, username, password, registration_date, role, temp, salt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            parameters = (first_name, last_name, username, hashed_password, registration_date, role.value, temp, salt)
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
            query = "DELETE FROM users WHERE id = ? AND role = ?"
            cursor.execute(query, (user_id, role.value))
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError(f"No user found with id {user_id} and role {role.value}")
            cursor.close()
            return "OK"
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the user: {e}")
            return "FAIL"
        except ValueError as ve:
            print(str(ve))

    def deleteMember(self, membership_id):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = "DELETE FROM members WHERE membership_id = ?"
            cursor.execute(query, (membership_id,))
            conn.commit()
            cursor.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while deleting the member:", e)
            return None
        finally:
            if conn:
                conn.close()

    def updateUser(self, userId, firstName, lastName, username, role):
        conn = None
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = """
            UPDATE users
            SET first_name = ?, last_name = ?, username = ?
            WHERE id = ? AND role = ?
            """
            parameters = (firstName, lastName, username, userId, role.value)
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            return "OK"
        except sqlite3.Error as e:
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
            query = "UPDATE members SET"
            parameters = []

            for field, value in fields.items():
                query += f" {field} = ?,"
                parameters.append(value)

            query = query.rstrip(",") + " WHERE membership_id = ?"
            parameters.append(membershipID)

            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            return "OK"
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
            query = "UPDATE users SET password = ?, temp = ?, salt = ? WHERE id = ?"
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

