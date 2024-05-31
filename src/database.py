from datetime import date
import sqlite3
from sqlite3 import Error
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

        # Check if super_admin user already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'super_admin'")
        user_exists = cursor.fetchone()[0] > 0

        if not user_exists:
            query = "INSERT INTO users (first_name, last_name, username, password, registration_date, role, temp) VALUES (?, ?, ?, ?, ?, ?, ?)"
            parameters = ("Babak", "Basharirad", "super_admin", "Admin_123!", date.today().strftime("%Y-%m-%d"), "superadmin", False)
            cursor.execute(query, parameters)
            conn.commit()
            print("Super admin user created")
        else:
            print("Super admin user already exists")

        cursor.close()
        conn.close()
