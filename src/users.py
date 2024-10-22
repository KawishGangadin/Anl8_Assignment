from enum import Enum
from datetime import date, datetime
import os
import time
from cryptoUtils import cryptoUtils
from inputValidation import Validation
from checkSum import Checksum
from roles import roles
from userBlueprint import userBlueprint


class consultant(userBlueprint):

    def memberCreation(self, db, loggingSys):
        try:
            print("""
1. Email Validation:
   - Must be in a valid email format (`username@domain.com`).

2. Age Validation:
   - Must be an integer between 1 and 100.

3. House Number Validation:
   - Must be an integer between 1 and 9999.

4. Zip Code Validation:
   - Must be exactly 6 characters long.
   - The first four characters must be digits (0-9).
   - The last two characters must be alphabetic.

5. Name Validation:
   - Must contain only alphabetic characters, hyphens, apostrophes, or spaces.
   - Maximum of one hyphen or apostrophe, and two spaces.
   - Cannot start or end with a hyphen or apostrophe.
   - Cannot be empty.

6. Mobile Number Validation:
   - Must be an integer between 1000000000 and 9999999999.

7. Membership ID Validation:
   - Must be an integer between 1000000000 and 9999999999.

8. Address Validation:
    - Must contain only alphanumeric characters, spaces, dots, commas, apostrophes, hyphens, or single quotes.
    - Cannot be empty.

9. City Validation:
    - Must be one of the following cities: Amsterdam, Rotterdam, The Hague, Utrecht, Eindhoven, Tilburg, Groningen, Almere, Breda, Nijmegen.
""")

            public_key = cryptoUtils.loadPublicKey()
            firstName = ""
            while not firstName:
                firstName = input("Enter the member's first name or press 'Q' to quit: ").strip()
                if firstName.upper() == 'Q':
                    return
                if not Validation.validateName(firstName, self.userName, loggingSys):
                    print("Invalid firstName!")
                    firstName = ""

            lastName = ""
            while not lastName:
                lastName = input("Enter the member's lastName or press 'Q' to quit: ").strip()
                if lastName.upper() == 'Q':
                    return
                if not Validation.validateName(lastName, self.userName, loggingSys):
                    print("Invalid lastName!")
                    lastName = ""

            age = ""
            while not age:
                age = input("Enter the member's age or press 'Q' to quit: ").strip()
                if age.upper() == 'Q':
                    return
                if not Validation.validateAge(age, self.userName, loggingSys):
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
                    if weight > 700:
                        print("Invalid weight!")
                        weight = ""
                except ValueError:
                    print("Invalid weight!")
                    weight = ""

            membershipId = Checksum.generateMembershipId(db)

            address = ""
            while not address:
                address = input("Enter the member's address or press 'Q' to quit: ").strip()
                if address.upper() == 'Q':
                    return
                if not Validation.validateAddress(address, self.userName, loggingSys):
                    print("Invalid address!")
                    address = ""

            city = ""
            while not city:
                city = input("Enter the member's city or press 'Q' to quit: ").strip()
                if city.upper() == 'Q':
                    return
                if not Validation.validateCity(city, self.userName, loggingSys):
                    print("Invalid city!")
                    city = ""

            postalCode = ""
            while not postalCode:
                postalCode = input("Enter the member's postal code or press 'Q' to quit: ").strip()
                if postalCode.upper() == 'Q':
                    return
                if not Validation.validateZipcode(postalCode, self.userName, loggingSys):
                    print("Invalid postal code!")
                    postalCode = ""

            email = ""
            while not email:
                email = input("Enter the member's email or press 'Q' to quit: ").strip()
                if email.upper() == 'Q':
                    return
                if not Validation.validateEmail(email, self.userName, loggingSys):
                    print("Invalid email address!")
                    email = ""

            mobile = ""
            while not mobile:
                mobile = input("Enter the member's mobile number +316..... or press 'Q' to quit: ").strip()
                if mobile.upper() == 'Q':
                    return
                if not Validation.validateMobileNumber(mobile, self.userName, loggingSys):
                    print("Invalid mobile number!")
                    mobile = ""

            registrationDate = date.today().strftime("%Y-%m-%d")

            result = db.createMember(firstName, lastName, age, gender, weight,
                                     address, city, postalCode,
                                     email, mobile, registrationDate, membershipId)
            if result == "OK":
                loggingSys.log("Member registered.", False, f"Member with membership ID '{membershipId}' has been registered.", self.userName)
                print("Member registered successfully.")
            else:
                print("An error occurred while registering the member.")
                loggingSys.log("Unsuccesful member registration", False, "An error occurred while registering the member.", self.userName)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log("Unsuccesful member registration", False, "An error occurred while registering the member.", self.userName)

    def displayMembers(self, db):
        try:
            allMembers = db.getMembers()
            private_key = cryptoUtils.loadPrivateKey()
            print(f"========List of Members====================================================================================================")
            if allMembers == None:
                print("No members found:")
            else:
                for member in allMembers:
                    print(f"| Membership ID: {(cryptoUtils.decryptWithPrivateKey(private_key,member[0])).decode('utf-8')} | First name: {(cryptoUtils.decryptWithPrivateKey(private_key,member[1])).decode('utf-8')} | Last name: {(cryptoUtils.decryptWithPrivateKey(private_key,member[2])).decode('utf-8')} | Age: {(cryptoUtils.decryptWithPrivateKey(private_key,member[3])).decode('utf-8')} | Gender: {(cryptoUtils.decryptWithPrivateKey(private_key,member[4])).decode('utf-8')} | Weight: {(cryptoUtils.decryptWithPrivateKey(private_key,member[5])).decode('utf-8')} | Address: {(cryptoUtils.decryptWithPrivateKey(private_key,member[6])).decode('utf-8')} | City: {(cryptoUtils.decryptWithPrivateKey(private_key,member[7])).decode('utf-8')} | Postal Code: {(cryptoUtils.decryptWithPrivateKey(private_key,member[8])).decode('utf-8')} | Email: {(cryptoUtils.decryptWithPrivateKey(private_key,member[9])).decode('utf-8')} | Mobile: {(cryptoUtils.decryptWithPrivateKey(private_key,member[10])).decode('utf-8')} | Registration Date: {member[11]} |\n")
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
            loggingSys.log(f"Error occurred during member search: {str(e)}", True, username=self.userName)

    def editMember(self, db, loggingSys):
        try:
            self.displayMembers(db)
            while True:
                membershipID = input("Enter the membership ID of the member you would like to edit or press Q to quit: ")
                if membershipID.upper() == "Q":
                    return
                if Validation.validateMembershipID(membershipID, self.userName, loggingSys) and db.findMembershipID(membershipID):
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
                "first_name": lambda value: Validation.validateName(value,self.userName,loggingSys),
                "last_name": lambda value: Validation.validateName(value,self.userName,loggingSys),
                "age": lambda value: Validation.validateAge(value,self.userName,loggingSys),
                "gender": lambda x: x in ["Male", "Female", "Other"],
                "weight": lambda value: value.replace('.', '', 1).isdigit() and float(value) > 0 and float(value) < 700,
                "address": lambda value: Validation.validateAddress(value,self.userName,loggingSys),
                "city": lambda value: Validation.validateCity(value,self.userName,loggingSys),
                "postalCode": lambda value: Validation.validateZipcode(value,self.userName,loggingSys),
                "email": lambda value: Validation.validateEmail(value,self.userName,loggingSys),
                "mobile": lambda value: Validation.validateMobileNumber(value,self.userName,loggingSys)
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
                loggingSys.log(f"Member with ID '{membershipID}' has been updated.", False, username=self.userName)
            else:
                print("Failed to update member.")
                loggingSys.log("Failed to update member.", True, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during member edit: {str(e)}", True, username=self.userName)

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
                    elif Validation.passwordValidation(password, self.userName, loggingSys):
                        data = db.getUserData(self.userName)
                        if data  != None:
                            storedPassword = data[4] 
                            storedSalt = data[8]  
                            if cryptoUtils.verifyPassword(password, storedPassword, storedSalt):
                                correctPassword = True
                                print("Password matches")
                                break
                            else:
                                print("Password does not match.")
                        else:
                            print("Something went wrong, user not found.")
                    else:
                        print("Please input a valid password...")

                while correctPassword:
                    newPassword = input("Please input your new password or press Q to quit: ")
                    if newPassword.upper() == "Q":
                        print("Exiting...")
                        time.sleep(0.5)
                        return
                    elif Validation.passwordValidation(newPassword, self.userName, loggingSys):
                        result = db.updatePassword(self.id, newPassword)
                        if result == "OK":
                            print("Password has been successfully changed!")
                            loggingSys.log("Password has been successfully changed.", False, username=self.userName)
                        else:
                            print("Failed to change password.")
                            loggingSys.log("Failed to change password.", True, username=self.userName)
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
            loggingSys.log(f"Error occurred during password change: {str(e)}", True, username=self.userName)
    
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
                        privateKey = cryptoUtils.loadPrivateKey()
                        deletedUsername = db.getUsernameByID(Id)
                        result = db.deleteUser(Id, role)
                        if result == "OK":
                            print("User deleted")
                            loggingSys.log("User deleted", False, f"User  '{cryptoUtils.decryptWithPrivateKey(privateKey,deletedUsername)}' has been deleted.", self.userName)
                            deletedUsername = None
                        else:
                            print("An error occurred while deleting the user.")
                            loggingSys.log("Failed to delete user", True, f"An error occurred while deleting the user : {cryptoUtils.decryptWithPrivateKey(privateKey,deletedUsername)}.", self.userName)
                            deletedUsername = None
                        time.sleep(1)
                    else:
                        result = db.deleteMember(Id)
                        if result == "OK":
                            print("Member deleted")
                            loggingSys.log("Member has been deleted", False, username=self.userName)
                        else:
                            print("An error occurred while deleting the member.")
                            loggingSys.log(f"Failed to delete member with id {Id}", True, username=self.userName)
                        time.sleep(1)
            if role is None:  
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
            loggingSys.log(f"Error occurred during deletion: {str(e)}", True, username=self.userName)


class systemAdministrator(consultant):
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
            loggingSys.log(f"Error occurred during backup creation: {str(e)}", True, username=self.userName)

    def userCreation(self, db, role, loggingSys):
        try:
            if role not in [roles.ADMIN, roles.CONSULTANT]:
                print("Invalid role")
                loggingSys.log("User tried to create a user with an invalid RoleType", True, username=self.userName)
                return

            roleType = role.value
            public_key = cryptoUtils.loadPublicKey()
            print(f"=========creating a {roleType} =========")

            def processCreation():
                validFL_Name = False
                availableUsername = False
                validPassword = False
                print("""
    1. Username Validation:
    - Must start with a letter or underscore.
    - Can contain letters, digits, underscores, apostrophes, or dots.
    - Length must be between 8 and 10 characters.

    2. Password Validation:
    - Must be between 12 and 30 characters.
    - Must include at least one lowercase letter, one uppercase letter, one digit, and one special character from `~!@#$%&_\-+=\|(){}[\]:;'<>,.?/`.
    3. Name Validation:
    - Must contain only alphabetic characters, hyphens, apostrophes, or spaces.
    - Maximum of one hyphen or apostrophe, and two spaces.
    - Cannot start or end with a hyphen or apostrophe.
    - Cannot be empty.
    """)

                while not validFL_Name:
                    firstName = input(f"Enter the first name of the new {roleType} or press Q to quit...\n")
                    if firstName.upper() == 'Q':
                        return
                    lastName = input(f"Enter the last name of the new {roleType} or press Q to quit...\n")
                    if lastName.upper() == 'Q':
                        return
                    if not Validation.validateName(firstName, self.userName, loggingSys) or not Validation.validateName(lastName, self.userName, loggingSys):
                        print("Please enter a valid first and lastname!!!")
                        loggingSys.log(f"User tried to create a {roleType} with either an invalid first name or last name", False, username=self.userName)
                        continue
                    else:
                        validFL_Name = True

                while not availableUsername:
                    username = input(f"Enter the username of the new {roleType} or press Q to quit...\n")
                    if username.upper() == 'Q':
                        return
                    if not Validation.usernameValidation(username, self.userName, loggingSys):
                        print("Please insert a valid username...")
                        loggingSys.log(f"User tried to create a {roleType} with an invalid username", False, username=self.userName)
                        continue
                    if db.findUsername(username.lower()):
                        print("Username already exists...")
                        loggingSys.log(f"User tried to create a {roleType} with an existing username", False, username=self.userName)
                    else:
                        print("Username is available!")
                        availableUsername = True

                while not validPassword:
                    password = input(f"Enter the password of the new {roleType} or press Q to quit...\n")
                    data = self.db.getUserData(username)
                    if password.upper() == 'Q':
                        return
                    if not Validation.passwordValidation(password, self.userName, loggingSys):
                        loggingSys.log(f"User tried to create a {roleType}: with an invalid password", False, username=self.userName)
                        continue
                    else:
                        validPassword = True
                        break

                creationDate = date.today().strftime("%Y-%m-%d")
                encryptedRole = cryptoUtils.encryptWithPublicKey(public_key,roleType)
                encryptedUsername = cryptoUtils.encryptWithPublicKey(public_key,username.lower())
                result = self.db.createUser(firstName, lastName, encryptedUsername, password, creationDate, encryptedRole, False)
                if result == "OK":
                    print(f"{roleType} created successfully.")
                    loggingSys.log(f"User has created a {roleType}", False, username=self.userName)
                else:
                    print(f"Failed to create {roleType}.")
                    loggingSys.log(f"Failed to create {roleType}", True, username=self.userName)
        except Exception as e:
            print(f"An error occurred while creating user: {str(e)}")
            loggingSys.log(f"Error occurred during user creation: {str(e)}", True, username=self.userName)

        processCreation()

    def displayUsers(self, db, role=None):
        try:
            allUsers = db.getUsers(role)
            title = "user" if role is None else f"{role.value}"
            print(f"======== List of {title}s ====================================================================================================")
            privateKey = cryptoUtils.loadPrivateKey()
            if allUsers is None or allUsers == []:
                print("No users found.")
            else:
                for user in allUsers:
                    if len(user) >= 7: 
                        print(f"| ID: {user[0]} | First name: {user[1]} | Last name: {user[2]} | Username: {(cryptoUtils.decryptWithPrivateKey(privateKey,user[3])).decode('utf-8')} | Registration Date: {user[5]} | Role: {(cryptoUtils.decryptWithPrivateKey(privateKey,user[6])).decode('utf-8')} |\n")
                    else:
                        print("Incomplete user data found, skipping display.")
            
            input("Press any key to continue...")
        
        except Exception as e:
            print(f"An error occurred while displaying users: {str(e)}")
    
    def displayLogs(self, loggingSys):
        try:
            print("====================Unique Meal Logs====================\n")
            loggingSys.printLogs()
            print("Press any key to continue...")
            keyPress = input()
        except Exception as e:
            print(f"An error occurred while displaying logs: {str(e)}")
            loggingSys.log(f"Error occurred during display logs: {str(e)}", True, username=self.userName)

    def alertLogs(self, loggingSys):
        try:
            if loggingSys.hasUncheckedSuspiciousLogs():
                print("There are new suspicious activities that havent been checked \nGo check the logs as soon as possible!!!")
            else:
                print("No new suspicious activities logged...")
        except Exception as e:
            print(f"An error occurred while sending log alert: {str(e)}")
            loggingSys.log(f"Error occurred during log alert: {str(e)}", True, username=self.userName)

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
                        if not Validation.validateName(firstName, self.userName, loggingSys):
                            print("Invalid first name!")
                        else:
                            break

                    while True:
                        lastName = input(f"Enter the new last name for user or press 'Q' to quit: ").strip()
                        if lastName.upper() == 'Q':
                            return
                        if not Validation.validateName(lastName, self.userName, loggingSys):
                            print("Invalid last name!")
                        else:
                            break

                    while True:
                        username = input(f"Enter the new username for user or press 'Q' to quit: ").strip()
                        if username.upper() == 'Q':
                            return
                        if not Validation.usernameValidation(username.lower(), self.userName, loggingSys):
                            print("Invalid username!")
                        elif db.findUsername(username.lower()):
                            print("Username already exists!")
                        else:
                            break
                    result = db.updateUser(userID, firstName, lastName, username.lower())
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
            loggingSys.log(f"Error occurred during user edit: {str(e)}", True, username=self.userName)
    
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
                        elif Validation.passwordValidation(password, self.userName, loggingSys):
                            result = db.updatePassword(userID, password, True)
                            
                            if result == "OK":
                                print("Password updated successfully.")
                                return
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
            loggingSys.log(f"Error occurred during password reset: {str(e)}", True, username=self.userName)

    def restoreBackup(self, backUpSystem, loggingSys):
        try:
            backUpSystem.listBackupNames()
            while True:
                name = input("Enter the file name of the backup to start restoring or press Q to quit...")
                if name.upper() == "Q":
                    print("Quitting...")
                    break
                else:
                    if not Validation.validateBackup(name,self.userName, loggingSys):
                        print("Please enter a valid file name!")
                    else:
                        print("Restoring backup....")
                        backUpSystem.restoreBackup(name)
                        break

        except Exception as e:
            print(f"An error occurred while restoring backup: {str(e)}")
            loggingSys.log(f"Error occurred during backup restoration: {str(e)}", True, username=self.userName)


class superAdministrator(systemAdministrator):
    pass