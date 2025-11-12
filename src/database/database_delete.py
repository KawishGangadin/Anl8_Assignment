from cryptoUtils import CryptoUtils
from inputValidation import InputValidation
from roles import roles
import users
import sqlite3

class DBDelete:
    
    def DeleteUser(self, user_id, role, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return "FAIL"
            if str(user_id).isdigit() and role.value in [roles.ADMIN.value, roles.SERVICE.value]:
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM users WHERE id = ?"
                cursor.execute(query, (user_id,))
                user = cursor.fetchone()
                
                if user is None:
                    raise ValueError(f"No user found with id {user_id}")
                
                private_key = CryptoUtils.LoadPrivateKey() 
                decrypted_role = CryptoUtils.DecryptWithPrivateKey(private_key, user[6])  
                
                if decrypted_role == role.value:
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
    
    def DeleteScooter(self, scooter_id, user, userContext):
        conn = None
        try:
            
            required_roles = [roles.ADMIN, roles.SUPERADMIN]
            if(self.AuthorizeAny(userContext,required_roles) == False):
                return "FAIL"
            
            if isinstance(user, users.SystemAdministrator):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM scooters WHERE id = ?"
                cursor.execute(query, (scooter_id,))
                scooter = cursor.fetchone()
                
                if scooter is None:
                    raise ValueError(f"No scooter found with id {scooter_id}")
                
                delete_query = "DELETE FROM scooters WHERE id = ?"
                cursor.execute(delete_query, (scooter_id,))
                conn.commit()
                
                if cursor.rowcount == 0:
                    raise ValueError(f"No scooter found with id {scooter_id}")
                
                cursor.close()
                return "OK"
            return "FAIL"
        
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the scooter: {e}")
            return "FAIL"
        except ValueError as ve:
            print(str(ve))
            return "FAIL"
        finally:
            if conn:
                conn.close()

    def DeleteTraveller(self, traveller_id, user, userContext):
        conn = None
        try:

            required_roles = [roles.ADMIN, roles.SUPERADMIN]
            if(self.AuthorizeAny(userContext,required_roles) == False):
                return "FAIL"
            
            if isinstance(user, users.SystemAdministrator):
                conn = sqlite3.connect(self.databaseFile)
                cursor = conn.cursor()
                query = "SELECT * FROM travellers WHERE customer_id = ?"
                cursor.execute(query, (traveller_id,))
                traveller = cursor.fetchone()
                
                if traveller is None:
                    raise ValueError(f"No traveller found with id {traveller_id}")
                
                delete_query = "DELETE FROM travellers WHERE customer_id = ?"
                cursor.execute(delete_query, (traveller_id,))
                conn.commit()
                
                if cursor.rowcount == 0:
                    raise ValueError(f"No traveller found with id {traveller_id}")
                
                cursor.close()
                return "OK"
            return "FAIL"
        
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the traveller: {e}")
            return "FAIL"
        except ValueError as ve:
            print(str(ve))
            return "FAIL"
        finally:
            if conn:
                conn.close()

    def DeleteRestoreCode(self,user,code, userContext):
        conn = None
        try:
            if(self.IsAuthorized(userContext) == False):
                return "FAIL"
            if isinstance(user, users.SuperAdministrator):
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

    def DeleteUserRestoreCodes(self, user_id, user, userContext):
        conn = None
        try:
            required_role = roles.SUPERADMIN
            if(self.AuthorizeAction(userContext,required_role) == False):
                return "FAIL"
            if isinstance(user, users.SystemAdministrator):
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
        finally:
            if conn:
                conn.close()