from cryptoUtils import cryptoUtils
from inputValidation import Validation
from roles import roles
import users
import sqlite3

class DBDelete:
    
    def deleteUser(self, user_id, role):
        conn = None
        try:
            if str(user_id).isdigit() and role.value in [roles.ADMIN.value, roles.SERVICE.value]:
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
    
    def deleteRestoreCode(self,user,code):
        conn = None
        try:
            if isinstance(user, users.superAdministrator):
                if code:
                    conn = sqlite3.connect(self.databaseFile)
                    cursor = conn.cursor()
                    query = "DELETE FROM restore_codes WHERE id = ?"
                    cursor.execute(query, (code,))
                    conn.commit()
                    
                    if cursor.rowcount == 0:
                        raise ValueError(f"No restore code found with value {code}")
                    
                    cursor.close()
                    return "OK"
                return "FAIL"
            else:
                raise ValueError("Only superadmin can delete restore codes.")
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the restore code: {e}")
            return "FAIL"
        except ValueError as ve:
            print(str(ve))
            return "FAIL"
        finally:
            if conn:
                conn.close()

    def deleteUserRestoreCodes(self, user_id, user):
        conn = None
        try:
            if isinstance(user, users.systemAdministrator):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "DELETE FROM restore_codes WHERE system_admin_id = ?"
                cursor.execute(query, (user_id,))
                conn.commit()

                
                cursor.close()
                return "OK"
        except sqlite3.Error as e:
            print(f"An error occurred while deleting restore codes for user {user_id}: {e}")
            return "FAIL"
        except ValueError as ve:
            print(str(ve))
            return "FAIL" 