from enum import Enum
from datetime import date, datetime
import os
import time
from cryptoUtils import cryptoUtils
from inputValidation import Validation
from checkSum import Checksum
from roles import roles
from userBlueprint import userBlueprint
from utility import Utility


class serviceEngineer(userBlueprint):

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
                    if isinstance(password, str) and Validation.checkNullByte(password):
                        if Validation.passwordValidation(password, self.userName, loggingSys):
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
                            loggingSys.log(f'Invalid password format (did not match pattern):', False, username=self.userName)
                    else:
                        print("Please input a valid password...")
                        loggingSys.log(f'Non-string input format or null byte detected in password:', True, username=self.userName)

                while correctPassword:
                    newPassword = input("Please input your new password or press Q to quit: ")
                    if newPassword.upper() == "Q":
                        print("Exiting...")
                        time.sleep(0.5)
                        return
                    if isinstance(password, str) and Validation.checkNullByte(password):
                        if Validation.passwordValidation(newPassword, self.userName, loggingSys):
                            result = db.updatePassword(self.id, newPassword)
                            if result == "OK":
                                self.session += 1
                                print("Password has been successfully changed!")
                                loggingSys.log("Password has been successfully changed.", False, username=self.userName)
                            else:
                                print("Failed to change password.")
                                loggingSys.log("Failed to change password.", True, username=self.userName)
                            time.sleep(0.5)
                            return
                        else:
                            print("Please input a valid password...")
                            loggingSys.log(f'Invalid password format (did not match pattern):', False, username=self.userName)
                    else:
                        print("Please input a valid password...")
                        loggingSys.log(f'Non-string input format or null byte detected in password:', True, username=self.userName)

            if isinstance(user, superAdministrator):
                print("Unauthorized access...")
                time.sleep(0.5)
                return
            elif isinstance(user, systemAdministrator):
                processChangePW()
                loggingSys.log(f"Password change", False, username=self.userName)
            elif isinstance(user, serviceEngineer):
                role = roles.CONSULTANT
                processChangePW()
                loggingSys.log(f"Password change", False, username=self.userName)
            else:
                print("Unauthorized access...")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during password change: {str(e)}", True, username=self.userName)

    def displayScooters(self, db, loggingSys):
        try:
            result = db.getScooters()
            if result:
                print("Results:")
                print("----------------")
                for row in result:
                    print(f"ID: {row[0]}" )
                    print(f"In service date: {row[1]}")
                    print(f"Brand: {row[2]}")
                    print(f"Model: {row[3]}")
                    print(f"Serial number: {row[4]}")
                    print(f"Top speed: {row[5]}")
                    print(f"Battery capacity: {row[6]}")
                    print(f"State of charge (current): {row[7]}")
                    print(f"State of charge min: {row[8]}")
                    print(f"State of charge max: {row[9]}")
                    print(f"Location: lat: {row[10]}, long: {row[11]}")
                    print(f"Out of service date: {row[12]}")
                    print(f"Mileage: {row[13]}")
                    print(f"Last maintenance date: {row[14]}")
                    print("----------------")
            else:
                print("No results found.")
            
            input("Press any key to continue...")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            

    def searchScooter(self, db, loggingSys):
        try:
            search_key = input("Enter the search key: ")
            if isinstance(search_key, str) and Validation.checkNullByte(search_key):
                if Validation.validate_length(search_key, loggingSys):
                    result = db.getScooterByAttribute(search_key)
                    if result:
                        print("Search Results:")
                        print("----------------")
                        for row in result:
                            print(f"ID: {row[0]}" )
                            print(f"In service date: {row[1]}")
                            print(f"Brand: {row[2]}")
                            print(f"Model: {row[3]}")
                            print(f"Serial number: {row[4]}")
                            print(f"Top speed: {row[5]}")
                            print(f"Battery capacity: {row[6]}")
                            print(f"State of charge (current): {row[7]}")
                            print(f"State of charge min: {row[8]}")
                            print(f"State of charge max: {row[9]}")
                            print(f"Location: lat: {row[10]}, long: {row[11]}")
                            print(f"Out of service date: {row[12]}")
                            print(f"Mileage: {row[13]}")
                            print(f"Last maintenance date: {row[14]}")
                            print("----------------")
                    else:
                        print("No results found.")
                    input("Press any key to continue...")
                else:
                    print("Please input a valid search key...")
                    loggingSys.log(f'Invalid search key format (too long):', False, username=self.userName)

            else:
                print("Please input a valid search key...")
                loggingSys.log(f'Non-string input format or null byte detected in search key:', True, username=self.userName)
                time.sleep(0.5)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during scooter search: {str(e)}", True, username=self.userName)

    def updateScooter(self, db, user, loggingSys):
        # TODO: validate id and update validation for edited attributes
        try:
            self.displayScooters(db, loggingSys)
            id = input("Enter the ID of the scooter you would like to edit:")
            if id.upper() == "Q":
                        return
            if isinstance(id, str) and Validation.checkNullByte(id):
                if Validation.validateID(id, loggingSys):
                    result = db.getScooterByID(id)
                    if result:
                        vFunctions = (
                            Validation.validate_soc, #soc
                            Validation.validate_soc, #soc min
                            Validation.validate_soc, #soc max
                            Validation.validate_lat, #lat
                            Validation.validate_long, #long
                            Validation.validate_oos, #out of service (bool)
                            Validation.validate_mileage, #mileage
                            Validation.validate_maintenance_date #last maintenance date
                        )
                        fNames = ("State of charge (current)", "State of charge min.", "State of charge max.", "Latitude", "Longitude",
                                  "Out of service", "Mileage", "Last maintenance date")
                        rFields = list(result[7:])
                        offset = 7 # skipping the first 7 fields

                        if isinstance(user, systemAdministrator) or isinstance(user, superAdministrator):
                            adminVFunctions = (
                                Validation.validateName, #validate brand name
                                Validation.validateName, #validate model name
                                Validation.validate_serial, # validate serial number
                                Validation.validate_speed, # top speed
                                Validation.validate_batterycap #battery cap
                            )
                            adminFNames = ("Brand", "Model", "Serial number", "Top speed", "Battery capacity")
                            vFunctions = adminVFunctions + vFunctions
                            fNames = adminFNames + fNames
                            rFields = list(result[2:])
                            offset = 2 # only skipping the first 2 fields

                        for i, (f, n, v) in enumerate(zip(rFields, fNames, vFunctions)):
                            fInput = "-"
                            print(f"{n}: {f}")
                            while True:
                                fInput = input(f"Enter a new value or press Enter to keep current value (Q to cancel):")
                                if fInput == "" or fInput == "Q": # exit loop
                                    break
                                if isinstance(fInput, str) and Validation.checkNullByte(fInput):
                                    if v(fInput):
                                        break
                                    else:
                                        print(f"Please input a valid {n}...")
                                        time.sleep(0.5)
                                        continue
                                else:
                                    loggingSys.log(f'Non-string input format or null byte detected in {n}:', True, username=self.userName)
                            if fInput == "":
                                continue
                            if fInput == "Q":
                                break

                            rFields[i] = fInput

                        rFields = list(result[1:offset]) + rFields
                        result = db.editScooter(id, rFields) 
                        if result == "OK":
                            return
                        else:
                            raise Exception(result)
                    else:
                        print("Scooter with ID not found...")
                        time.sleep(0.5)
                else:
                    print("Please input a valid id...")
                    loggingSys.log(f'Invalid search key format:', False, username=self.userName)
            else:
                print("Please input a vald id...")
                loggingSys.log(f'Non-string input format or null byte detected in search key:', True, username=self.userName)

        except Exception as e:
            print(f"An error occurred during scooter update:", e)
            loggingSys.log(f"Error occurred during scooter update: {str(e)}", True, username=self.userName)
            return

class systemAdministrator(serviceEngineer):

    def createScooter(self, db, loggingSys):
        # TODO: validate id and update validation for edited attributes
        try:
                vFunctions = (
                    Validation.validateName, #validate brand name
                    Validation.validateName, #validate model name
                    Validation.validate_serial, # validate serial number
                    Validation.validate_speed, # top speed
                    Validation.validate_batterycap, #battery cap
                    Validation.validate_soc, #soc
                    Validation.validate_soc, #soc min
                    Validation.validate_soc, #soc max
                    Validation.validate_lat, #lat
                    Validation.validate_long, #long
                    Validation.validate_oos, #out of service (bool)
                    Validation.validate_mileage, #mileage
                    Validation.validate_maintenance_date #last maintenance date
                )
                fNames = ("Brand", "Model", "Serial number", "Top speed", "Battery capacity", "State of charge (current)",
                          "State of charge min.", "State of charge max.", "Latitude", "Longitude",
                          "Out of service", "Mileage", "Last maintenance date")

                fields = []

                for i, (n, v) in enumerate(zip(fNames, vFunctions)):
                    fInput = "-"
                    print(f"{n}:")
                    while True:
                        fInput = input(f"Enter a value (Q to cancel):")
                        if fInput == "Q":
                            return
                        if isinstance(fInput, str) and Validation.checkNullByte(fInput):
                            if v(fInput):
                                fields.append(fInput)
                                break
                            else:
                                loggingSys.log()
                        else:
                            loggingSys.log()
                        print("Invalid input")

                result = db.createScooter(fields)
                if result == "OK":
                    return
                else:
                    raise Exception(result)


        except Exception as e:
            print(f"An error occurred during scooter update:", e)
            loggingSys.log(f"Error occurred during scooter update: {str(e)}", True, username=self.userName)
            return

    def removeScooter(self, db, loggingSys):
        pass

    def createTraveller(self, db, role, loggingSys):
        try:
            print("======= Traveller Registration =======")

            inputs = {
            "first_name": ("Enter traveller's first name", Validation.validateName),
            "last_name": ("Enter traveller's last name", Validation.validateName),
            "birthdate": ("Enter traveller's birthdate (YYYY-MM-DD)", Validation.validate_birthdate),
            "gender": ("Enter traveller's gender (male/female/other)", Validation.validateGender),
            "street": ("Enter traveller's street name", Validation.validateAddress),
            "house_number": ("Enter traveller's house number", Validation.validateHousenumber),
            "zip_code": ("Enter traveller's zip code (e.g. 1234AB)", Validation.validateZipcode),
            "city": ("Enter traveller's city", Validation.validateCity),
            "email": ("Enter traveller's email", Validation.validateEmail),
            "mobile": ("Enter traveller's mobile number (8 digits)", Validation.validateMobileNumber),
             }

            values = {}
            for key, (prompt, validator) in inputs.items():
                value = Utility.get_valid_input(f"{prompt} or Q to quit:", validator, {'username': self.userName}, loggingSys)
                if value is None:
                    return
                values[key] = value

            # Handle license_number separately (no validator)
            license_number = input("Enter traveller's driving license number or Q to quit: ").strip()
            if license_number.upper() == "Q":
                return

            registration_date = date.today().strftime("%Y-%m-%d")
            customer_id = Checksum.generateMembershipId(db)
            
            result = db.createTraveller(
            customer_id,
            registration_date,
            values["first_name"],
            values["last_name"],
            values["birthdate"],
            values["gender"],
            values["street"],
            int(values["house_number"]),
            values["city"],
            values["zip_code"],
            values["email"],
            values["mobile"],
            license_number
            )


            if result == "OK":
                print("Traveller registered successfully.")
                loggingSys.log("Traveller registered", False, f"Traveller with ID {customer_id} registered.", self.userName)
            else:
                print("An error occurred while registering the traveller.")
                loggingSys.log("Failed to register traveller", True, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Exception during traveller registration: {str(e)}", True, username=self.userName)


    def updateTraveller(self, db, loggingSys):
        def safe_decrypt(value):
            try:
                if isinstance(value, bytes):
                    return cryptoUtils.decryptWithPrivateKey(private_key, value).decode()
                return str(value)
            except:
                return "(decryption failed)"

        # Display all decrypted travellers
        travellers = db.getAllTravellers()
        private_key = cryptoUtils.loadPrivateKey()

        print("\n======= Registered Travellers =======")
        for t in travellers:
            try:
                print(f"ID: {t[0]}")
                print(f"Name: {safe_decrypt(t[2])} {safe_decrypt(t[3])}")
                print(f"Birthdate: {t[4]}")
                print(f"Gender: {safe_decrypt(t[5])}")
                print(f"Street: {safe_decrypt(t[6])} {safe_decrypt(t[7])}")
                print(f"City: {safe_decrypt(t[8])}")
                print(f"Zip: {safe_decrypt(t[9])}")
                print(f"Email: {safe_decrypt(t[10])}")
                print(f"Mobile: {safe_decrypt(t[11])}")
                print(f"License: {safe_decrypt(t[12])}")
                print("-------------------------------------")
            except:
                print("(Unable to decrypt one or more fields)")

        license_number = Utility.get_valid_input("Enter the traveller's current driving license number or Q to cancel:", Validation.validate_driving_license, {'username': self.userName}, loggingSys)
        if license_number is None:
            print("Update cancelled.")
            return

        if not db.licenseExists(license_number):
            print("No traveller found with that license number.")
            return

        fields = {}

        print("\nUpdating traveller fields. Leave empty to skip a field or Q to quit.")

        new_first = Utility.get_optional_update("New first name:", Validation.validateName, None, {'username': self.userName}, loggingSys)
        if new_first == "Q": return
        if new_first: fields["first_name"] = new_first

        new_last = Utility.get_optional_update("New last name:", Validation.validateName, None, {'username': self.userName}, loggingSys)
        if new_last == "Q": return
        if new_last: fields["last_name"] = new_last

        new_gender = Utility.get_optional_update("New gender:", Validation.validateGender, None, {'username': self.userName}, loggingSys)
        if new_gender == "Q": return
        if new_gender: fields["gender"] = new_gender

        new_street = Utility.get_optional_update("New street name:", Validation.validateAddress, None, {'username': self.userName}, loggingSys)
        if new_street == "Q": return
        if new_street: fields["street_name"] = new_street

        new_house = Utility.get_optional_update("New house number:", Validation.validateHousenumber, None, {'username': self.userName}, loggingSys)
        if new_house == "Q": return
        if new_house: fields["house_number"] = new_house

        new_city = Utility.get_optional_update("New city:", Validation.validateCity, None, {'username': self.userName}, loggingSys)
        if new_city == "Q": return
        if new_city: fields["city"] = new_city

        new_zip = Utility.get_optional_update("New zip code:", Validation.validateZipcode, None, {'username': self.userName}, loggingSys)
        if new_zip == "Q": return
        if new_zip: fields["zip_code"] = new_zip

        new_email = Utility.get_optional_update("New email:", Validation.validateEmail, None, {'username': self.userName}, loggingSys)
        if new_email == "Q": return
        if new_email: fields["email"] = new_email

        new_mobile = Utility.get_optional_update("New mobile number:", Validation.validateMobileNumber, None, {'username': self.userName}, loggingSys)
        if new_mobile == "Q": return
        if new_mobile: fields["mobile"] = new_mobile

        new_license = Utility.get_optional_update("New license number:", Validation.validate_driving_license, None, {'username': self.userName}, loggingSys)
        if new_license == "Q": return
        if new_license and new_license != license_number:
            if db.licenseExists(new_license):
                print("That license number is already in use.")
                return
            fields["license_number"] = new_license

        result = db.updateTraveller(license_number, **fields)

        if result == "OK":
            print("Traveller updated successfully.")
            loggingSys.log("Traveller updated", False, username=self.userName)
        elif result == "NOT FOUND":
            print("Traveller not found.")
        else:
            print("An error occurred while updating the traveller.")
            loggingSys.log("Traveller update failed", True, username=self.userName)


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
            print(f"=========creating a {roleType} =========")

            def processCreation():
                validF_Name = False
                validL_Name = False
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

                while not validF_Name:
                    firstName = input(f"Enter the first name of the new {roleType} or press Q to quit...\n")
                    if firstName.upper() == 'Q':
                        return
                    if not Validation.validateName(firstName, self.userName, loggingSys):
                        print("Please enter a valid firstname!!!")
                        loggingSys.log(f"User tried to create a {roleType} with either an invalid first name or last name", False, username=self.userName)
                        continue
                    else:
                        validF_Name = True

                while not validL_Name:
                    lastName = input(f"Enter the last name of the new {roleType} or press Q to quit...\n")
                    if lastName.upper() == 'Q':
                        return
                    if not Validation.validateName(lastName, self.userName, loggingSys):
                        print("Please enter a valid lastname!!!")
                        loggingSys.log(f"User tried to create a {roleType} with either an invalid first name or last name", False, username=self.userName)
                        continue
                    else:
                        validL_Name = True

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
                        print("Please enter a valid password!!!")
                        loggingSys.log(f"User tried to create a {roleType}: with an invalid password", False, username=self.userName)
                        continue
                    else:
                        validPassword = True
                        break

                creationDate = date.today().strftime("%Y-%m-%d")
                result = self.db.createUser(firstName, lastName, username, password, creationDate, role, False)
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
                        print(f"| ID: {user[0]} | First name: {user[1]} | Last name: {user[2]} | Username: {user[3]} | Registration Date: {user[5]} | Role: {user[6]} |\n")
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

    def restoreBackup(self, backUpSystem, loggingSys,db):
        try:
            backUpSystem.listBackupNames()
            if isinstance(self, superAdministrator):
                while True:
                    name = input("Enter the name of the backup file to restore or press Q to quit: ").strip()
                    if name.upper() == "Q":
                        print("Quitting...")
                        break

                    if not Validation.validateBackup(name, self.userName, loggingSys):
                        print("Please enter a valid backup filename!")
                        continue

                    print("Restoring backup as Super Administrator...")
                    backUpSystem.restoreBackup(name, username=self.userName)
                    break
                return
            elif isinstance(self, systemAdministrator):
                codes = db.getRestoreCodesByUser(self.id)
                if not codes:
                    print("No restore codes found for your account.")
                    return

                print("\nYour restore codes:")
                for code, filename in codes:
                    print(f"- Code: {code} | Backup: {filename}")
                print()

                while True:
                    name = input("Enter the name of the backup file to restore or press Q to quit: ").strip()
                    if name.upper() == "Q":
                        print("Quitting...")
                        break

                    if not Validation.validateBackup(name, self.userName, loggingSys):
                        print("Please enter a valid backup filename!")
                        continue

                    code = input("Enter your restore code or press Q to quit: ").strip()
                    if code.upper() == "Q":
                        print("Quitting...")
                        break

                    if (code, name) in codes:
                        print("Restore code valid. Restoring backup...")
                        backUpSystem.restoreBackup(name, username=self.userName)
                        break
                    else:
                        print("Invalid restore code or backup mismatch.")

            else:
                print("Unauthorized user type. You are not allowed to restore backups.")

        except Exception as e:
            print(f"An error occurred while restoring backup: {str(e)}")
            loggingSys.log(f"Error occurred during backup restoration: {str(e)}", True, username=self.userName)


class superAdministrator(systemAdministrator):
    def generateRestoreCode(self, db, loggingSys):
        try:
            self.displayUsers(db, roles.ADMIN)

            while True:
                admin_id = input("Enter the ID of the System Administrator to generate a restore code for, or press Q to quit: ").strip()
                if admin_id.upper() == "Q":
                    return
                if admin_id.isdigit() and db.findUserID(int(admin_id), roles.ADMIN):
                    admin_id = int(admin_id)
                    break
                else:
                    print("Invalid ID or not a System Administrator!")
                    time.sleep(0.5)

            backup_name = input("Enter the exact name of the backup file (e.g., backup_20240601_1700.zip) or press Q to quit: ").strip()
            if backup_name.upper() == "Q":
                return

            if not os.path.isfile(os.path.join("backups", backup_name)):
                print("Backup file not found.")
                return

            code = db.createRestoreCode(admin_id, backup_name)
            if code != "FAIL":
                print(f"Restore code generated successfully: {code}")
                loggingSys.log("Restore code generated", False, f"Restore code for backup '{backup_name}' assigned to user ID {admin_id}.", self.userName)
            else:
                print("Failed to generate restore code.")
                loggingSys.log("Restore code generation failed", True, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during restore code generation: {str(e)}", True, username=self.userName)
