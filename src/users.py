from enum import Enum
from datetime import date, datetime
import os
import time
from cryptoUtils import cryptoUtils
from inputValidation import Validation
from checkSum import Checksum
class roles(Enum):
    CONSULTANT = 'consultant'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'


class userBlueprint:
    def __init__(self, id, userName,db):
        self.id = id
        self.userName = userName
        self.db = db 

class consultant(userBlueprint):

    def memberCreation(self, db, loggingSys):
        try:
            firstName = ""
            while not firstName:
                firstName = input("Enter the member's first name or press 'Q' to quit: ").strip()
                if firstName.upper() == 'Q':
                    return
                if not Validation.validateName(firstName):
                    print("Invalid firstName!")
                    firstName = ""

            lastName = ""
            while not lastName:
                lastName = input("Enter the member's lastName or press 'Q' to quit: ").strip()
                if lastName.upper() == 'Q':
                    return
                if not Validation.validateName(lastName):
                    print("Invalid lastName!")
                    lastName = ""

            membershipId = Checksum.generateMembershipId(db)

            age = ""
            while not age:
                age = input("Enter the member's age or press 'Q' to quit: ").strip()
                if age.upper() == 'Q':
                    return
                if not Validation.validateAge(age):
                    print("Invalid age!")
                    age = ""

            gender = ""
            while not gender:
                gender = input("Enter the member's gender (Male/Female/Other) or press 'Q' to quit: ").strip().capitalize()
                if gender.upper() == 'Q':
                    return
                if gender not in ['Male', 'Female', 'Other']:
                    print("Invalid gender!")
                    gender = ""

            weight = ""
            while not weight:
                weight = input("Enter the member's weight or press 'Q' to quit: ").strip()
                if weight.upper() == 'Q':
                    return
                try:
                    weight = float(weight)
                    if weight < 0:
                        print("Weight must be a positive number!")
                        weight = ""
                except ValueError:
                    print("Invalid weight!")
                    weight = ""

            address = ""
            while not address:
                address = input("Enter the member's address or press 'Q' to quit: ").strip()
                if address.upper() == 'Q':
                    return
                if not Validation.validateAddress(address):
                    print("Invalid address!")
                    address = ""

            city = ""
            while not city:
                city = input("Enter the member's city or press 'Q' to quit: ").strip()
                if city.upper() == 'Q':
                    return
                if not Validation.validateCity(city):
                    print("Invalid city!")
                    city = ""

            postalCode = ""
            while not postalCode:
                postalCode = input("Enter the member's postal code or press 'Q' to quit: ").strip()
                if postalCode.upper() == 'Q':
                    return
                if not Validation.validateZipcode(postalCode):
                    print("Invalid postal code!")
                    postalCode = ""

            email = ""
            while not email:
                email = input("Enter the member's email or press 'Q' to quit: ").strip()
                if email.upper() == 'Q':
                    return
                if not Validation.validateEmail(email):
                    print("Invalid email address!")
                    email = ""

            mobile = ""
            while not mobile:
                mobile = input("Enter the member's mobile number or press 'Q' to quit: ").strip()
                if mobile.upper() == 'Q':
                    return
                if not Validation.validateMobileNumber(mobile):
                    print("Invalid mobile number!")
                    mobile = ""

            registrationDate = date.today().strftime("%Y-%m-%d")

            # All input checks passed, now create the member
            result = db.createMember(firstName, lastName, age, gender, weight, address, city, postalCode, email, mobile, registrationDate, membershipId)
            if result == "OK":
                loggingSys.log(f"Member '{firstName} {lastName}' has been registered with membership ID '{membershipId}'", False)
                print("Member registered successfully.")
            else:
                print("An error occurred while registering the member.")
                loggingSys.log("Failed to register a member", True)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during member creation: {str(e)}", True)

    def deletion(self, user, db, role, loggingSys):
        try:
            def processDeletion(role):
                roleType = ""
                if role == None:
                    self.displayMembers(db)
                    roleType = "member"
                else:
                    self.displayUsers(db, role)
                    roleType = role.value
                validID = False
                while True:
                    Id = input(f"Enter the ID/membership ID of the {roleType} you would like to delete or enter 'Q' to quit: ").strip()
                    if Id.upper() == "Q":
                        return
                    elif Id.isdigit():
                        if not role == None:
                            if db.findUserID(int(Id), role):
                                validID = True
                                break
                        else:
                            if db.findMembershipID(Id):
                               validID = True
                               break 
                    print("ID not found in the database!" if Id.isdigit() else "ID is invalid!")
                    time.sleep(0.5)
                if validID:
                    if not role == None:
                        result = db.deleteUser(Id, role)
                        if result == "OK":
                            print("User deleted")
                            loggingSys.log("User has been deleted", False)
                        else:
                            print("An error occurred while deleting the user.")
                            loggingSys.log("Failed to delete user", True)
                        time.sleep(1)
                    else:
                        result = db.deleteMember(Id)
                        if result == "OK":
                            print("Member deleted")
                            loggingSys.log("Member has been deleted", False)
                        else:
                            print("An error occurred while deleting the member.")
                            loggingSys.log("Failed to delete member", True)
                        time.sleep(1)
            if role is None:  # Consultant role
                if isinstance(user, consultant):
                    processDeletion(role)
                else:
                    print("Unauthorized access...")
            elif isinstance(user, superAdministrator):
                if role in [None, roles.CONSULTANT, roles.ADMIN]:
                    processDeletion(role)
                else:
                    print("Invalid request....")
            elif isinstance(user, systemAdministrator):
                if role in [None, roles.CONSULTANT]:
                    processDeletion(role)
                else:
                    print("Unauthorized request.")
            else:
                print("Unauthorized access...")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during deletion: {str(e)}", True)

    def displayMembers(self, db):
        try:
            allMembers = db.getMembers()
            
            print(f"========List of Members====================================================================================================")
            if allMembers == None:
                print("No members found:")
            else:
                for member in allMembers:
                    print(f"| Membership ID: {member[0]} | First name: {member[1]} | Last name: {member[2]} | Age: {member[3]} | Gender: {member[4]} | Weight: {member[5]} | Address: {member[6]} | City: {member[7]} | Postal Code: {member[8]} | Email: {member[9]} | Mobile: {member[10]} | Registration Date: {member[11]} |\n")
            input("Press any key to continue...")
            return
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def memberSearch(self, db, loggingSys):
        try:
            search_key = input("Enter the search key: ")
            result = db.searchMember(search_key)
            if result:
                print("Search Results:")
                print("----------------")
                for row in result:
                    print(f"Membership ID: {row[0]}")
                    print(f"First Name: {row[1]}")
                    print(f"Last Name: {row[2]}")
                    print(f"Age: {row[3]}")
                    print(f"Gender: {row[4]}")
                    print(f"Weight: {row[5]}")
                    print(f"Address: {row[6]}")
                    print(f"City: {row[7]}")
                    print(f"Postal Code: {row[8]}")
                    print(f"Email: {row[9]}")
                    print(f"Mobile: {row[10]}")
                    print(f"Registration Date: {row[11]}")
                    print("----------------")
            else:
                print("No results found.")
            input("Press any key to continue...")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during member search: {str(e)}", True)

    def editMember(self, db, loggingSys):
        try:
            self.displayMembers(db)
            while True:
                membershipID = input("Enter the membership ID of the member you would like to edit or press Q to quit: ")
                if membershipID.upper() == "Q":
                    return
                if Validation.validateMembershipID(membershipID) and db.findMembershipID(membershipID):
                    break
                else:
                    print("Invalid membership ID!!!")

            def getValidInput(prompt, validation_func):
                while True:
                    user_input = input(prompt).strip()
                    if user_input.upper() == "Q":
                        return "Q"
                    if user_input == "" or validation_func(user_input):
                        return user_input
                    else:
                        print("Invalid input!!!")

            updates = {}
            fields_validations = {
                "first_name": Validation.validateName,
                "last_name": Validation.validateName,
                "age": Validation.validateAge,
                "gender": lambda x: x in ["Male", "Female", "Other"],
                "weight": lambda x: x.replace('.', '', 1).isdigit() and float(x) > 0,
                "address": Validation.validateAddress,
                "city": Validation.validateCity,
                "postalCode": Validation.validateZipcode,
                "email": Validation.validateEmail,
                "mobile": Validation.validateMobileNumber
            }
            for field, validation in fields_validations.items():
                input_value = getValidInput(f"Enter new {field.replace('_', ' ')} or leave empty to make no changes: ", validation)
                if input_value == "Q":
                    print("Edit process terminated by user.")
                    return
                if input_value:
                    updates[field] = int(input_value) if field == "age" else float(input_value) if field == "weight" else input_value

            result = db.updateMember(membershipID, **updates)
            if result == "OK":
                print("Member updated successfully.")
                loggingSys.log(f"Member with ID '{membershipID}' has been updated.", False)
            else:
                print("Failed to update member.")
                loggingSys.log("Failed to update member.", True)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during member edit: {str(e)}", True)

    def changePassword(self, user, db, loggingSys):
        try:
            def processChangePW():
                correctPassword = False
                while True:
                    password = input("Input your current password or press Q to quit: ")
                    if password.upper() == "Q":
                        print("Exiting...")
                        time.sleep(0.5)
                        return
                    elif Validation.passwordValidation(password):
                        print("Password validated")
                        print(self.userName)
                        data = db.getUserData(self.userName)
                        if data  != None:
                            print("data is not none")
                            storedPassword = data[4]  # Assuming hashedPassword is stored in the 5th column
                            storedSalt = data[8]  # Assuming salt is stored in the 9th column
                            print(storedSalt)
                            if cryptoUtils.verifyPassword(password, storedPassword, storedSalt):
                                correctPassword = True
                                print("Password matches")
                                break
                            else:
                                print("Password does not match.")
                        else:
                            print("Password does not match.")
                    else:
                        print("Please input a valid password...")

                while correctPassword:
                    newPassword = input("Please input your new password or press Q to quit: ")
                    if newPassword.upper() == "Q":
                        print("Exiting...")
                        time.sleep(0.5)
                        return
                    elif Validation.passwordValidation(newPassword):
                        result = db.updatePassword(self.id, newPassword)
                        if result == "OK":
                            print("Password has been successfully changed!")
                            loggingSys.log("Password has been successfully changed.", False)
                        else:
                            print("Failed to change password.")
                            loggingSys.log("Failed to change password.", True)
                        time.sleep(0.5)
                        return
                    else:
                        print("Please input a valid password...")

            if isinstance(user, superAdministrator):
                print("Unauthorized access...")
                time.sleep(0.5)
                return
            elif isinstance(user, systemAdministrator):
                processChangePW()
            elif isinstance(user, consultant):
                role = roles.CONSULTANT
                processChangePW()
            else:
                print("Unauthorized access...")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during password change: {str(e)}", True)


class systemAdministrator(consultant):

    def displayUsers(self, db, role=None):
        try:
            allUsers = db.getUsers(role)
            title = "user" if role is None else f"{role.value}"
            print(f"========List of {title}s====================================================================================================")
            if allUsers is None:
                print("No users found:")
            else:
                for user in allUsers:
                    print(f"| ID: {user[0]} | First name: {user[1]} | Last name {user[2]} | Username: {user[3]} | Registration Date: {user[5]} | Role: {user[6]} |\n")
            input("Press any key to continue...")
        except Exception as e:
            print(f"An error occurred while displaying users: {str(e)}")

    def editUser(self, user, db, role, loggingSys):
        try:
            def processEdit(role):
                self.displayUsers(db, role)
                validID = False
                userID = ""
                while True:
                    userID = input(f"Enter the ID of the {role.value} you would like to edit or enter 'Q' to quit: ").strip()
                    if userID.upper() == "Q":
                        return
                    elif userID.isdigit() and db.findUserID(int(userID), role):
                        validID = True
                        break
                    else:
                        print("ID not found in the database!" if userID.isdigit() else "ID is invalid!")
                        time.sleep(0.5)

                if validID:
                    while True:
                        firstName = input(f"Enter the new first name for user or press 'Q' to quit: ").strip()
                        if firstName.upper() == 'Q':
                            return
                        if not Validation.validateName(firstName):
                            print("Invalid first name!")
                        else:
                            break

                    while True:
                        lastName = input(f"Enter the new last name for user or press 'Q' to quit: ").strip()
                        if lastName.upper() == 'Q':
                            return
                        if not Validation.validateName(lastName):
                            print("Invalid last name!")
                        else:
                            break

                    while True:
                        username = input(f"Enter the new username for user or press 'Q' to quit: ").strip()
                        if username.upper() == 'Q':
                            return
                        if not Validation.usernameValidation(username):
                            print("Invalid username!")
                        elif db.findUsername(username):
                            print("Username already exists!")
                        else:
                            break

                    # Update the user in the database
                    result = db.updateUser(int(userID), firstName, lastName, username, role)
                    if result == "OK":
                        print("User information updated successfully.")
                    else:
                        print("Failed to update user information.")

            if isinstance(user, superAdministrator):
                if role in [roles.ADMIN, roles.CONSULTANT]:
                    processEdit(role)
                else:
                    print("Invalid request....")
            elif isinstance(user, systemAdministrator):
                if role == roles.CONSULTANT:
                    processEdit(role)
                else:
                    print("Unauthorized request.")
            else:
                print("Unauthorized access...")

        except Exception as e:
            print(f"An error occurred while editing user: {str(e)}")
            loggingSys.log(f"Error occurred during user edit: {str(e)}", True)

    def displayLogs(self, loggingSys):
        try:
            print("====================Unique Meal Logs====================\n")
            loggingSys.printLogs()
            print("Press any key to continue...")
            keyPress = input()
        except Exception as e:
            print(f"An error occurred while displaying logs: {str(e)}")
            loggingSys.log(f"Error occurred during display logs: {str(e)}", True)

    def createBackup(self, user, backUpSystem, loggingSys):
        try:
            while True:
                keyPress = input("Would you like to create a back up [Y/N] ")
                if keyPress.upper() == "Y":
                    print("Creating backup....")
                    backUpSystem.createBackupZip(user)
                    break
                elif keyPress.upper() == "N":
                    print("Exiting.....")
                    break
                else:
                    print("Invalid input...")

        except Exception as e:
            print(f"An error occurred while creating backup: {str(e)}")
            loggingSys.log(f"Error occurred during backup creation: {str(e)}", True)

    def restoreBackup(self, backUpSystem, loggingSys):
        try:
            backUpSystem.listBackupNames()
            while True:
                name = input("Enter the file name of the backup to start restoring or press Q to quit...")
                if name.upper() == "Q":
                    print("Quitting...")
                    break
                else:
                    print("Restoring backup....")
                    backUpSystem.restoreBackup(name)

        except Exception as e:
            print(f"An error occurred while restoring backup: {str(e)}")
            loggingSys.log(f"Error occurred during backup restoration: {str(e)}", True)

    def resetPassword(self, user, db, role, loggingSys):
        try:
            def processReset(role):
                self.displayUsers(db, role)
                validID = False
                userID = ""
                
                while True:
                    userID = input(f"Enter the ID of the {role.value} you would like to edit or enter 'Q' to quit: ").strip()
                    
                    if userID.upper() == "Q":
                        return
                    elif userID.isdigit() and db.findUserID(int(userID), role):
                        validID = True
                        break
                    else:
                        print("ID not found in the database!" if userID.isdigit() else "ID is invalid!")
                        time.sleep(0.5)
                
                if validID:
                    while True:
                        password = input("Enter the new temporary password for the user or press Q to quit: ").strip()
                        
                        if password.upper() == "Q":
                            print("Exiting...")
                            time.sleep(0.5)
                            return
                        elif Validation.passwordValidation(password):
                            result = db.updatePassword(int(userID), password, True)
                            
                            if result == "OK":
                                print("Password updated successfully.")
                            else:
                                print("Failed to update password.")
                                
                        else:
                            print("Please enter a valid password!")
            
            if isinstance(user, superAdministrator):
                if role in [roles.ADMIN, roles.CONSULTANT]:
                    processReset(role)
                else:
                    print("Invalid request.")
            elif isinstance(user, systemAdministrator):
                if role == roles.CONSULTANT:
                    processReset(role)
                else:
                    print("Unauthorized request.")
            else:
                print("Unauthorized access.")

        except Exception as e:
            print(f"An error occurred while resetting password: {str(e)}")
            loggingSys.log(f"Error occurred during password reset: {str(e)}", True)


    def userCreation(self, db, role, loggingSys):
        try:
            if role not in [roles.ADMIN, roles.CONSULTANT]:
                print("Invalid role")
                loggingSys.log("User tried to create a user with an invalid RoleType", True)
                return

            roleType = role.value
            print(f"=========creating a {roleType} =========")

            def processCreation():
                validFL_Name = False
                availableUsername = False
                validPassword = False

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
                    data = self.db.getUserData(username)
                    if password.upper() == 'Q':
                        return
                    if not Validation.passwordValidation(password):
                        loggingSys.log(f"User tried to create a {roleType}: {username} with an invalid password", True)
                        continue
                    else:
                        validPassword = True
                        break

                creationDate = date.today().strftime("%Y-%m-%d")
                result = db.createUser(firstName, lastName, username, password, creationDate, role, False)
                if result == "OK":
                    print(f"{roleType} created successfully.")
                    loggingSys.log(f"User has created a {roleType}", False)
                else:
                    print(f"Failed to create {roleType}.")
                    loggingSys.log(f"Failed to create {roleType}", True)

            processCreation()

        except Exception as e:
            loggingSys.log(f"An error occurred during user creation: {str(e)}", True)
            print(f"An error occurred: {str(e)}")

class superAdministrator(systemAdministrator):
    pass