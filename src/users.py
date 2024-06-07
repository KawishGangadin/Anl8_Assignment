from enum import Enum
from datetime import date
import time
from inputValidation import Validation
class roles(Enum):
    CONSULTANT = 'consultant'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'


class userBlueprint:
    def __init__(self, id, userName):
        self.id = id
        self.userName = userName

class consultant(userBlueprint):
    def consultantMenu(self):
        print("""[1] Search members
[2] Register member
[3] Update member info
[4] Update password\n""")


class systemAdministrator(consultant):
    def administratorMenu(self):
        pass
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

    def userCreation(self, db, role, loggingSys):
        roleType = ""
        if role in [roles.ADMIN, roles.CONSULTANT]:
            roleType = role.value
        else:
            print("Invalid role")
            loggingSys.log("User tried to create a user with an invalid RoleType", True)
            return
        
        print(f"=========creating a {roleType} =========")
        
        availableUsername = False
        validPassword = False
        validFL_Name = False
        while not validFL_Name:
            firstName = input(f"Enter the first name of the new {roleType} or press Q to quit...\n")
            if firstName.upper() == 'Q':
                return
            lastName = input(f"Enter the last name of the new {roleType} or press Q to quit...\n")
            if lastName.upper() == 'Q':
                return
            if not Validation.validateName(firstName) or not Validation.validateName(lastName):
                loggingSys.log(f"User tried to create a {roleType} with either an invalid first name or last name", True)
                continue
            else:
                validFL_Name = True

        while not availableUsername:
            username = input(f"Enter the username of the new {roleType} or press Q to quit...\n")
            if username.upper() == 'Q':
                return
            if not Validation.usernameValidation(username):
                loggingSys.log(f"User tried to create a {roleType} with an invalid username", True)
                continue
            if db.findUsername(username):
                loggingSys.log(f"User tried to create a {roleType} with an existing username", False)
            else:
                availableUsername = True
        
        while not validPassword:
            password = input(f"Enter the password of the new {roleType} or press Q to quit...\n")
            if password.upper() == 'Q':
                return
            if not Validation.passwordValidation(password):
                loggingSys.log(f"User tried to create a {roleType}: {username} with an invalid password", True)
                continue
            else:
                validPassword = True

        creationDate = date.today().strftime("%Y-%m-%d")
        db.createUser(firstName, lastName, username, password, creationDate, roleType, False)
        loggingSys.log(f"User has created a {roleType}", False)