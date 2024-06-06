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
            parameters = ("Babak", "Basharirad", "super_admin", "Admin_123!", date.today().strftime("%Y-%m-%d"), "superadmin", False)
            cursor.execute(query, parameters)
            conn.commit()
        else:
            pass

        cursor.close()
        conn.close()
    
    def getUserData(self, username, password):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "SELECT * FROM users"
        cursor.execute(query)

        users = cursor.fetchall()
        for userData in users:
            if username == userData[3] and password == userData[4]:
                return userData
            else:
                pass

        return None

    def findID(self, id):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "SELECT * FROM members"
        cursor.execute(query)
        
        users = cursor.fetchall()
        exists = False
        if users != None:
            for IDs in users:
                print(IDs[0], id)
                if IDs[0] == id:
                    return True
        return False
    
    def findUsername(self, username):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = "SELECT * FROM users"
        cursor.execute(query)
        
        users = cursor.fetchall()
        if users != None:
            for usernames in users:
                if usernames[3] == username:
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