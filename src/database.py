from datetime import date
import sqlite3
from sqlite3 import Error
from users import roles
import time

class DB:
    def __init__(self,databaseFile) -> None:
        self.databaseFile = databaseFile

    def create_members_table(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER CHECK(age >= 0),
            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
            weight REAL CHECK(weight >= 0),
            address TEXT,
            email TEXT UNIQUE NOT NULL,
            mobile TEXT UNIQUE NOT NULL,
            registration_date DATE NOT NULL,
            membership_id TEXT UNIQUE NOT NULL
        )
        """
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        cursor.execute(create_query)
        conn.commit()
        cursor.close()
        conn.close()

    def create_users_table(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            registration_date DATE NOT NULL,
            role TEXT CHECK(role IN ('admin', 'consultant', 'superadmin')) NOT NULL,
            temp BOOLEAN NOT NULL CHECK(temp IN (0, 1))
        )
        """
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        cursor.execute(create_query)
        conn.commit()
        cursor.close()
        conn.close()

    def init_superadmin(self):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'super_admin'")
        user_exists = cursor.fetchone()[0] > 0

        if not user_exists:
            query = "INSERT INTO users (first_name, last_name, username, password, registration_date, role, temp) VALUES (?, ?, ?, ?, ?, ?, ?)"
            parameters = ("Kawish", "Gangadin", "super_admin", "Admin_123?", date.today().strftime("%Y-%m-%d"), "superadmin", False)
            cursor.execute(query, parameters)
            conn.commit()
        else:
            pass

        cursor.close()
        conn.close()
    
    def searchMember(self, search_key):
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = """
            SELECT * FROM members 
            WHERE 
                id LIKE ? OR
                first_name LIKE ? OR
                last_name LIKE ? OR
                address LIKE ? OR
                email LIKE ? OR
                mobile LIKE ?
            """
            # Constructing search patterns for partial matches
            search_pattern = '%' + search_key + '%'
            parameters = (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)
            
            cursor.execute(query, parameters)
            members = cursor.fetchall()
            cursor.close()
            conn.close()
            return members
        except sqlite3.Error as e:
            print("An error occurred while searching members:", e)
            return None

    def getUserData(self, username, password):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query,(username,password,))

        users = cursor.fetchall()
        if users:
            for user in users:
                return user
        else:
            return None

    def findID(self, id):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "SELECT * FROM members WHERE id = ?"
        cursor.execute(query, (id,))
        
        user = cursor.fetchone()  # Fetch one row
        
        if user is not None:
            return True  # Member ID exists
        else:
            return False  # Member ID does not exist

    
    def findUserID(self, id,role):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE role = ?"
        cursor.execute(query, (role.value,))
        
        users = cursor.fetchall()
        exists = False
        if users != None:
            for IDs in users:
                if IDs[0] == id:
                    return True
        return False
    
    def findUsername(self, username):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query,(username,))
        
        users = cursor.fetchall()
        if users:
            return True
        return False

    def getUsers(self, role):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        if role == None:
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            if users != None:
                return users
            return None
        elif role == roles.CONSULTANT:
            query = "SELECT * FROM users WHERE role = ?"
            cursor.execute(query, (role.value,))
            users = cursor.fetchall()
            if users != None:
                return users
            return None
        elif role == roles.ADMIN:
            query = "SELECT * FROM users WHERE role = ?"
            cursor.execute(query, (role.value,))
            users = cursor.fetchall()
            if users != None:
                return users
            return None
        else:
            return None
    
    def getMembers(self):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "SELECT * FROM members"
        cursor.execute(query)
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return members

    def createMember(self, first_name, last_name, age, gender, weight, address, email, mobile, registration_date, membership_id):
        conn = sqlite3.connect(self.databaseFile)
        query = """
        INSERT INTO members (first_name, last_name, age, gender, weight, address, email, mobile, registration_date, membership_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (first_name, last_name, age, gender, weight, address, email, mobile, registration_date, membership_id)
        cursor = conn.cursor()

        try:
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            conn.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while creating the member:", e)
            cursor.close()
            conn.close()
            return None


    def createUser(self, first_name, last_name, username, password, registration_date, role, temp):
        conn = sqlite3.connect(self.databaseFile)
        query = "INSERT INTO users (first_name, last_name, username, password, registration_date, role, temp) VALUES (?, ?, ?, ?, ?, ?, ?)"
        parameters = (first_name, last_name, username, password, registration_date, role, temp)
        cursor = conn.cursor()

        try:
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            conn.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while creating the user:", e)
            cursor.close()
            conn.close()
            return None
        
    def deleteUser(self, userID, role):
        conn = sqlite3.connect(self.databaseFile)
        query = "DELETE FROM users WHERE id = ? AND role = ?"
        parameters = (userID, role.value)
        cursor = conn.cursor()
        try:
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            conn.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while deleting the user:", e)
            cursor.close()
            conn.close()
            return None
        
    def deleteMember(self, id):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "DELETE FROM members WHERE id = ?"
        parameters = (id,)
        try:
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            conn.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while deleting the member:", e)
            cursor.close()
            conn.close()
            return None


    def updateUser(self, userId, firstName, lastName, username, role):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = """
        UPDATE users
        SET first_name = ?, last_name = ?, username = ?
        WHERE id = ? AND role = ?
        """
        parameters = (firstName, lastName, username, userId, role.value)
        try:
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            conn.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while updating the user:", e)
            cursor.close()
            conn.close()
            return None