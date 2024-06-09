from datetime import date
import sqlite3
from sqlite3 import Error
from users import roles
import time
import os
from datetime import datetime
import zipfile
import shutil

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
    
    def updateUserPassword(self, userId, tempPassword, role):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        query = """
        UPDATE users
        SET password = ?, temp = 1
        WHERE id = ? AND role = ?
        """
        parameters = (tempPassword, userId, role.value)
        try:
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            conn.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while updating the user password:", e)
            cursor.close()
            conn.close()
            return None
        
    def get_log_files(self):
        log_files = []
        log_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(log_dir, 'logs', 'uniquemeal.log')
        if os.path.exists(log_file):
            log_files.append(log_file)
        return log_files

    def createBackup(self, backup_dir='backups'):
        # create backup dir if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        # timestamp for the filename (file can be overridden if backup made multiple times in a second)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{timestamp}.zip"
        backup_filepath = os.path.join(backup_dir, backup_filename)

        log_files = self.get_log_files()

        # temporary directory to store files
        temp_dir = os.path.join(backup_dir, f"temp_{timestamp}")
        os.makedirs(temp_dir)
        for log_file in log_files: # dump log files
            with open(log_file, 'r') as f:
                log_content = f.read()
            log_backup_path = os.path.join(temp_dir, os.path.basename(log_file))
            with open(log_backup_path, 'w') as f:
                f.write(log_content)

        # dump database
        db_dump_path = os.path.join(temp_dir, 'database_dump.sql')
        with sqlite3.connect(self.databaseFile) as conn:
            with open(db_dump_path, 'w') as f:
                for line in conn.iterdump():
                    f.write('%s\n' % line)
        
        # zip the log files
        with zipfile.ZipFile(backup_filepath, 'w') as backup_zip:
            backup_zip.write(db_dump_path, os.path.basename(db_dump_path))
            for log_file in log_files:
                log_backup_path = os.path.join(temp_dir, os.path.basename(log_file))
                backup_zip.write(log_backup_path, os.path.basename(log_backup_path))

        # remove temporary directory
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

        return backup_filepath
    
    def getBackupList(self, backup_dir='backups'):
        backup_files = []
        if os.path.exists(backup_dir):
            backup_files = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))] # get all files in backup directory
        return backup_files
    
    def restoreBackup(self, backup_filepath):
        # extract backup zip in temporary directory
        temp_dir = os.path.join(os.path.dirname(backup_filepath), 'restore_temp')
        os.makedirs(temp_dir)
        with zipfile.ZipFile(backup_filepath, 'r') as backup_zip:
            backup_zip.extractall(temp_dir)

        # get file paths
        extracted_files = os.listdir(temp_dir)
        db_dump_file = None
        log_files = []
        for file in extracted_files:
            if file == 'database_dump.sql':
                db_dump_file = os.path.join(temp_dir, file)
            else:
                log_files.append(os.path.join(temp_dir, file))

        # clear database tables
        with sqlite3.connect(self.databaseFile) as conn:
            conn.execute("DROP TABLE IF EXISTS members")
            conn.execute("DROP TABLE IF EXISTS users")

        if db_dump_file: # restore database
            with sqlite3.connect(self.databaseFile) as conn:
                with open(db_dump_file, 'r') as f:
                    conn.executescript(f.read())
        for log_file in log_files: # restore log files
            target_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', os.path.basename(log_file))
            with open(log_file, 'r') as fsrc:
                with open(target_log_path, 'w') as fdst:
                    fdst.write(fsrc.read())

        # remove temporary directory
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

        return "OK"

