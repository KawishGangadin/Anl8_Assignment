from enum import Enum
from datetime import date
import time
class roles(Enum):
    CONSULTANT = 'consultant'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'


class userBlueprint:
    def __init__(self, id, userName):
        self.id = id
        self.userName = userName

class consultant(userBlueprint):
    pass

class systemAdministrator(consultant):
    def displayUsers(self,db,role=None):
        allUsers = db.getUsers(role)
        title = ""
        if role == None:
            title = "user"
        else:
            title = f"{role.value}"
        print(f"========List of {title}s====================================================================================================")
        if allUsers == None:
            print("No users found:")
        else:
            for user in allUsers:
                print(f"| ID: {user[0]} | First name: {user[1]} | Last name {user[2]} | Username: {user[3]} | Registration Date: {user[5]} | Role: {user[6]} |\n")
        input("Press any key to continue...")
        return
    
    def editUser(self, user, db, role):
        if isinstance(user, superAdministrator):
            if role == roles.ADMIN:
                self.displayUsers(db, role)
                validID = False
                while True:
                    ID = input(f"Enter the ID of the {role.value} you would like to edit or enter 'Q' to quit: ").strip()
                    if ID.upper() == "Q":
                        return
                    elif ID.isdigit():
                        if db.findUserID(int(ID), role):
                            validID = True
                            break
                        else:
                            print("ID not found in the database!")
                    else:
                        print("ID is invalid!")
                    time.sleep(0.5)

                if validID:
                    print("hello")

            elif role == roles.CONSULTANT:
                self.displayUsers(db, role)
                validID = False
                while True:
                    ID = input(f"Enter the ID of the {role.value} you would like to edit or enter 'Q' to quit: ").strip()
                    if ID.upper() == "Q":
                        return
                    elif ID.isdigit():
                        if db.findUserID(int(ID), role):
                            validID = True
                            break
                        else:
                            print("ID not found in the database!")
                    else:
                        print("ID is invalid!")
                    time.sleep(0.5)

                if validID:
                    print("hello")

            else:
                print("Invalid request....")
                return

        elif isinstance(user, systemAdministrator):
            if role == roles.CONSULTANT:
                self.displayUsers(db, role)
                validID = False
                while True:
                    ID = input(f"Enter the ID of the {role.value} you would like to edit or enter 'Q' to quit: ").strip()
                    if ID.upper() == "Q":
                        return
                    elif ID.isdigit():
                        if db.findUserID(int(ID), role):
                            validID = True
                            break
                        else:
                            print("ID not found in the database!")
                    else:
                        print("ID is invalid!")
                    time.sleep(0.5)

                if validID:
                    print("hello")

            else:
                print("Unauthorized request.")
                return

        else:
            print("Unauthorized access...")
            return

            
        
class superAdministrator(systemAdministrator):

    def testFunc(self):
        print("hello")
        time.sleep(2)

    def userCreation(self,db,role):
        roleType = ""
        if role == roles.ADMIN:
            roleType = role.value
        elif role == roles.CONSULTANT:
            roleType = role.value
        else:
            print("Invalid role")
            exit()
        print(f"=========creating a {roleType} =========")
        availableUsername = False
        firstName = input(f"Enter the first name of the new {roleType} \n")
        lastName = input(f"Enter the last name of the new {roleType} \n")
        while availableUsername == False:
            username = input(f"Enter the username of the new {roleType} \n")
            if not db.findUsername(username):
                availableUsername = True
            else:
                availableUsername = False
        password = input(f"Enter the password of the new {roleType} \n")
        creationDate =date.today().strftime("%Y-%m-%d")
        db.createUser(firstName,lastName,username,password,creationDate,roleType,False)
    
