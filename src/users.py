from enum import Enum
from datetime import date, datetime
import os
import random
import string
import time
from cryptoUtils import cryptoUtils
from inputValidation import Validation
from checkSum import Checksum
from roles import roles
from userBlueprint import userBlueprint
from utility import Utility


class service(userBlueprint):

    def changePassword(self, db, loggingSys):
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

            if isinstance(self, superAdministrator):
                print("Unauthorized access...")
                time.sleep(0.5)
                return
            elif isinstance(self, systemAdministrator):
                processChangePW()
            elif isinstance(self, service):
                role = roles.SERVICE
                processChangePW()
            else:
                print("Unauthorized access...")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during password change: {str(e)}", True, username=self.userName)

    def editScooter(self,db, loggingSys):
        try:
            db.displayAllScooters()

            while True:
                scooter_id = input("Enter the ID of the scooter you want to edit or press 'Q' to quit: ").strip()
                if scooter_id.upper() == 'Q':
                    return
                if not scooter_id.isdigit():
                    print("Invalid ID format.")
                    continue

                scooter_id = int(scooter_id)
                if db.getScooterById(scooter_id):
                    break
                else:
                    print("Scooter ID not found.")

            editable_fields = {
                "brand": Validation.validateBrandOrModel,
                "model": Validation.validateBrandOrModel,
                "serial_number": Validation.validateSerialNumber,
                "top_speed": lambda v, u, l: Validation.validateIntegerInRange(v, 5, 120),
                "battery_capacity": lambda v, u, l: Validation.validateIntegerInRange(v, 100, 2000),
                "state_of_charge": lambda v, u, l: Validation.validateIntegerInRange(v, 0, 100),
                "target_soc_min": lambda v, u, l: Validation.validateIntegerInRange(v, 0, 100),
                "target_soc_max": lambda v, u, l: Validation.validateIntegerInRange(v, 0, 100),
                "mileage": lambda v, u, l: Validation.validateIntegerInRange(v, 0, 999999),
                "last_maintenance_date": lambda v, u, l: Validation.validate_birthdate(v)
            }

            if self.role == roles.SERVICE:
                allowed = {"state_of_charge", "target_soc_min", "target_soc_max", "mileage", "last_maintenance_date"}
            else:
                allowed = set(editable_fields.keys()).union({"latitude", "longitude"})

            updated = {}

            for field, validator in editable_fields.items():
                if field not in allowed:
                    continue
                value = Utility.get_optional_update(
                    f"Update {field.replace('_', ' ').title()}",
                    validator,
                    "(hidden)",
                    user={"username": self.userName},
                    loggingSys=loggingSys
                )
                if value == "Q":
                    print("Cancelled editing.")
                    return
                elif value != "(hidden)":
                    updated[field] = value

            if "latitude" in allowed and "longitude" in allowed:
                while True:
                    lat = input("Enter new latitude or leave empty to keep current (or Q to quit): ").strip()
                    if lat.upper() == "Q":
                        print("Cancelled editing.")
                        return

                    lon = input("Enter new longitude or leave empty to keep current (or Q to quit): ").strip()
                    if lon.upper() == "Q":
                        print("Cancelled editing.")
                        return

                    if not lat and not lon:
                        break

                    if Validation.validateCoordinates(lat, lon, self.userName, loggingSys):
                        updated["latitude"] = lat
                        updated["longitude"] = lon
                        break
                    else:
                        print("Invalid coordinates. Try again or leave both empty.")

            if updated:
                if db.updateScooter(scooter_id, updated) == "OK":
                    print("Scooter updated successfully.")
                    loggingSys.log("Scooter edited", False, f"Scooter ID {scooter_id} edited.", self.userName)
                else:
                    print("Failed to update scooter.")
                    loggingSys.log("Scooter edit failed", True, f"Scooter ID {scooter_id} update failed.", self.userName)
            else:
                print("No changes were made.")

        except Exception as e:
            print(f"An error occurred while editing scooter: {str(e)}")
            loggingSys.log(f"Error occurred during scooter editing: {str(e)}", True, username=self.userName)

    def searchScooter(self, db, loggingSys):
        try:
            search_term = input("Enter the search key: ")
            result = db.searchScooter(search_term)
            
            if result:
                print("Search Results:")
                print("----------------")
                for row in result:
                    print(f"Scooter ID: {row[0]} | In Service Date: {row[1]} | Brand: {row[2]} | Model: {row[3]} | Serial Number: {row[4]} | Top Speed: {row[5]} km/h | Battery Capacity: {row[6]} Wh | State of Charge: {row[7]}% | Target SOC Min: {row[8]}% | Target SOC Max: {row[9]}% | Latitude: {row[10]} | Longitude: {row[11]} | Out of service: {row[12]} | Mileage: {row[13]} km | Last Maintenance Date: {row[14]}")
                    print("----------------")
            else:
                print("No results found.")
            
            input("Press any key to continue...")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during scooter search: {str(e)}", True, username=self.userName)

class systemAdministrator(service):

    def searchTraveller(self, db, loggingSys):
        try:
            search_term = input("Enter the search key: ")
            result = db.searchTraveller(search_term)
            
            if result:
                print("Search Results:")
                print("----------------")
                for row in result:
                    print(f"Customer ID: {row[0]} | Registration Date: {row[1]} | First Name: {row[2]} | Last Name: {row[3]} | Birthdate: {row[4]} | Gender: {row[5]} | Street: {row[6]} | House Number: {row[7]} | City: {row[8]} | Zip Code: {row[9]} | Email: {row[10]} | Mobile: {row[11]} | License Number: {row[12]}")
                    print("----------------")
            else:
                print("No results found.")
            
            input("Press any key to continue...")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during scooter search: {str(e)}", True, username=self.userName)

    def deleteTraveller(self, db, loggingSys):
        try:
            db.displayAllTravellers()

            while True:
                traveller_id = input("Enter the ID of the scooter you want to edit or press 'Q' to quit: ").strip()
                if traveller_id.upper() == 'Q':
                    return
                if not traveller_id.isdigit():
                    print("Invalid ID format.")
                    continue

                traveller_id = int(traveller_id)
                if db.getTravellerById(traveller_id):
                    break
                else:
                    print("Scooter ID not found.")
            
            if db.deleteTraveller(traveller_id, self)  == "OK":
                print("Traveller deleted successfully.")
                loggingSys.log("Traveller deleted", False, f"Traveller ID {traveller_id} deleted.", self.userName)
            else:
                print("Failed to delete traveller.")
                loggingSys.log("Traveller deletion failed", True, f"Traveller ID {traveller_id} deletion failed.", self.userName)
        except Exception as e:
            print(f"An error occurred while deleting traveller: {str(e)}")
            loggingSys.log(f"Error occurred during traveller deletion: {str(e)}", True, username=self.userName)

    def deleteScooter(self, db, loggingSys):
        try:
            db.displayAllScooters()

            while True:
                scooter_id = input("Enter the ID of the scooter you want to edit or press 'Q' to quit: ").strip()
                if scooter_id.upper() == 'Q':
                    return
                if not scooter_id.isdigit():
                    print("Invalid ID format.")
                    continue

                scootetraveller_idr_id = int(scooter_id)
                if db.getScooterById(scooter_id):
                    break
                else:
                    print("Scooter ID not found.")
            
            if db.deleteScooter(scooter_id, self)  == "OK":
                print("Traveller deleted successfully.")
                loggingSys.log("Traveller deleted", False, f"Traveller ID {scooter_id} deleted.", self.userName)
            else:
                print("Failed to delete traveller.")
                loggingSys.log("Traveller deletion failed", True, f"Traveller ID {scooter_id} deletion failed.", self.userName)
        except Exception as e:
            print(f"An error occurred while deleting traveller: {str(e)}")
            loggingSys.log(f"Error occurred during traveller deletion: {str(e)}", True, username=self.userName)

    def deletion(self, db, role, loggingSys):
        try:
            def processDeletion(role):
                self.displayUsers(db, role)
                roleType = role.value

                validID = False
                while True:
                    Id = input(f"Enter the ID of the {roleType} you would like to delete or enter 'Q' to quit: ").strip()
                    if Id.upper() == "Q":
                        return

                    if not Id.isdigit():
                        print("ID is invalid!")
                        time.sleep(0.5)
                        continue

                    Id = int(Id)
                    if db.findUserID(Id, role):
                        validID = True
                        break
                    else:
                        print("ID not found in the database!")
                        time.sleep(0.5)

                if validID:
                    privateKey = cryptoUtils.loadPrivateKey()
                    deletedUsername = db.getUsernameByID(Id)
                    db.deleteUserRestoreCodes(Id,self)
                    result = db.deleteUser(Id, role)
                    if result == "OK":
                        print("User deleted.")
                        loggingSys.log("User deleted", False, f"User '{deletedUsername}' has been deleted.", self.userName)
                    else:
                        print("An error occurred while deleting the user.")
                        loggingSys.log("Failed to delete user", True, f"An error occurred while deleting the user: {deletedUsername}.", self.userName)
                    time.sleep(1)

            if isinstance(self, superAdministrator):
                if role in [roles.ADMIN, roles.SERVICE]:
                    processDeletion(role)
                else:
                    print("Invalid request...")
            elif isinstance(self, systemAdministrator):
                if role == roles.SERVICE:
                    processDeletion(role)
                else:
                    print("Unauthorized request.")
            elif isinstance(self, service):
                print("You are not authorized to delete any users.")
            else:
                print("Unauthorized access...")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during deletion: {str(e)}", True, username=self.userName)

    def createTraveller(self, db, role, loggingSys):
        try:
            print("========== Traveller Registration ==========")
            traveller = {}

            traveller["first_name"] = Utility.get_valid_input("Enter traveller's first name:",
                Validation.validateName, self.userName, loggingSys, "First Name")
            traveller["last_name"] = Utility.get_valid_input("Enter traveller's last name:",
                Validation.validateName, self.userName, loggingSys, "Last Name")
            traveller["birthdate"] = Utility.get_valid_input("Enter traveller's birthdate (YYYY-MM-DD):",
                Validation.validate_birthdate, self.userName, loggingSys, "Birthdate")
            traveller["gender"] = Utility.get_valid_input("Enter traveller's gender (male/female/other):",
                Validation.validateGender, self.userName, loggingSys, "Gender")
            traveller["street"] = Utility.get_valid_input("Enter traveller's street name:",
                Validation.validateAddress, self.userName, loggingSys, "Street")
            traveller["house_number"] = Utility.get_valid_input("Enter traveller's house number:",
                Validation.validateHousenumber, self.userName, loggingSys, "House Number")
            traveller["city"] = Utility.get_valid_input("Enter traveller's city:",
                Validation.validateCity, self.userName, loggingSys, "City")
            traveller["zip_code"] = Utility.get_valid_input("Enter traveller's zip code (e.g. 1234AB):",
                Validation.validateZipcode, self.userName, loggingSys, "Zip Code")
            traveller["email"] = Utility.get_valid_input("Enter traveller's email:",
                Validation.validateEmail, self.userName, loggingSys, "Email")
            traveller["mobile"] = Utility.get_valid_input("Enter traveller's mobile number (8 digits):",
                Validation.validateMobileNumber, self.userName, loggingSys, "Mobile Number")
            traveller["license_number"] = Utility.get_valid_input("Enter traveller's license number:",
                Validation.validate_driving_license, self.userName, loggingSys, "License Number")

            traveller["registration_date"] = date.today().strftime("%Y-%m-%d")
            traveller["customer_id"] = Checksum.generateMembershipId(db)

            result = db.createTraveller(traveller)

            if result == "OK":
                print("Traveller registered successfully.")
                loggingSys.log("Traveller registered", False, f"Traveller with ID {traveller['customer_id']} registered.", self.userName)
            else:
                print("Failed to register traveller.")
                loggingSys.log("Failed to register traveller", True, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Exception during traveller registration: {str(e)}", True, username=self.userName)

    def createScooter(self, db, loggingSys):
        try:
            print("========== Scooter Registration ==========")
            scooter = {}

            scooter["serial_number"] = Utility.get_valid_input("Enter serial number (SC-XXXXXX):",
                Validation.validateSerialNumber, self.userName, loggingSys, "Serial Number")
            scooter["brand"] = Utility.get_valid_input("Enter scooter brand:",
                Validation.validateBrandOrModel, self.userName, loggingSys, "Brand")
            scooter["model"] = Utility.get_valid_input("Enter scooter model:",
                Validation.validateBrandOrModel, self.userName, loggingSys, "Model")
            scooter["top_speed"] = Utility.get_valid_input("Enter top speed (km/h):",
                lambda v: Validation.validateIntegerInRange(v, 5, 120), self.userName, loggingSys, "Top Speed")
            scooter["battery_capacity"] = Utility.get_valid_input("Enter battery capacity (Wh):",
                lambda v: Validation.validateIntegerInRange(v, 100, 2000), self.userName, loggingSys, "Battery Capacity")
            scooter["state_of_charge"] = Utility.get_valid_input("Enter current charge (0-100):",
                lambda v: Validation.validateIntegerInRange(v, 0, 100), self.userName, loggingSys, "State of Charge")
            scooter["target_soc_min"] = Utility.get_valid_input("Enter minimum charge threshold (0-100):",
                lambda v: Validation.validateIntegerInRange(v, 0, 100), self.userName, loggingSys, "Target SOC Min")
            scooter["target_soc_max"] = Utility.get_valid_input(f'Enter maximum charge threshold ({scooter["target_soc_min"]}-100):',
                lambda v: Validation.validateIntegerInRange(v, int(scooter["target_soc_min"]), 100), self.userName, loggingSys, "Target SOC Max")
            scooter["mileage"] = Utility.get_valid_input("Enter current mileage (default 0):",
                lambda v: Validation.validateIntegerInRange(v, 0, 999999), self.userName, loggingSys, "Mileage")
            scooter["latitude"] = Utility.get_valid_input("Enter scooter latitude model (e.g. 51.92250):",
                Validation.validateLatitude, self.userName, loggingSys, "Latitude ")
            scooter["longtitude"] = Utility.get_valid_input("Enter scooter longtitude model (e.g. 4.47917):",
                Validation.validateLongitude, self.userName, loggingSys, "Longitude")

            scooter["in_service_date"] = datetime.today().strftime("%Y-%m-%d")
            scooter["last_maintenance_date"] = scooter["in_service_date"]

            result = db.createScooter(scooter)

            if result == "OK":
                print("Scooter registered successfully.")
                loggingSys.log("Scooter registered", False, f"Serial: {scooter['serial_number']}", self.userName)
            else:
                print("Failed to register scooter.")
                loggingSys.log("Scooter registration failed", True, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {e}")
            loggingSys.log(f"Scooter creation error: {str(e)}", True, username=self.userName)

    def createBackup(self, backUpSystem, loggingSys):
        try:
            while True:
                keyPress = input("Would you like to create a back up [Y/N] ")
                if keyPress.upper() == "Y":
                    print("Creating backup....")
                    backUpSystem.createBackupZip(self)
                    time.sleep(5)
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
            if role not in [roles.ADMIN, roles.SERVICE]:
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

    def editTraveller(self, db, loggingSys):
        try:
            db.displayAllTravellers()

            while True:
                traveller_id = input("Enter the ID of the traveller you want to edit or press 'Q' to quit: ").strip()
                if traveller_id.upper() == 'Q':
                    return

                if db.getTravellerById(traveller_id):
                    break
                else:
                    print("Traveller ID not found.")

            editable_fields = {
                "first_name": Validation.validateName,
                "last_name": Validation.validateName,
                "birthdate": Validation.validate_birthdate,
                "gender": Validation.validateGender,
                "street_name": Validation.validateAddress,
                "house_number": Validation.validateHousenumber,
                "city": Validation.validateCity,
                "zip_code": Validation.validateZipcode,
                "email": Validation.validateEmail,
                "mobile": Validation.validateMobileNumber,
                "license_number": Validation.validate_driving_license
            }

            updated = {}
            for field, validator in editable_fields.items():
                value = Utility.get_optional_update(
                    f"Update {field.replace('_', ' ').title()}",
                    validator,
                    "(hidden)",
                    user={"username": self.userName},
                    loggingSys=loggingSys
                )
                if value == "Q":
                    print("Cancelled editing.")
                    return
                elif value != "(hidden)":
                    updated[field] = value

            if updated:
                if db.updateTraveller(traveller_id, updated) == "OK":
                    print("Traveller updated successfully.")
                    loggingSys.log("Traveller edited", False, f"Traveller ID {traveller_id} edited.", self.userName)
                else:
                    print("Failed to update traveller.")
                    loggingSys.log("Traveller edit failed", True, f"Traveller ID {traveller_id} update failed.", self.userName)
            else:
                print("No changes were made.")

        except Exception as e:
            print(f"An error occurred while editing traveller: {str(e)}")
            loggingSys.log(f"Error occurred during traveller editing: {str(e)}", True, username=self.userName)

    def editUser(self, db, role, loggingSys):
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

            if isinstance(self, superAdministrator):
                if role in [roles.ADMIN, roles.SERVICE]:
                    processEdit(role)
                else:
                    print("Invalid request....")
            elif isinstance(self, systemAdministrator):
                if role == roles.SERVICE:
                    processEdit(role)
                else:
                    print("Unauthorized request.")
            else:
                print("Unauthorized access...")

        except Exception as e:
            print(f"An error occurred while editing user: {str(e)}")
            loggingSys.log(f"Error occurred during user edit: {str(e)}", True, username=self.userName)
    
    def resetPassword(self, db, role, loggingSys):
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
            
            if isinstance(self, superAdministrator):
                if role in [roles.ADMIN, roles.SERVICE]:
                    processReset(role)
                else:
                    print("Invalid request.")
            elif isinstance(self, systemAdministrator):
                if role == roles.SERVICE:
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

    def accountDeletion(self,db, loggingSys):
        try:
            if isinstance(self, superAdministrator):
                print("Super Administrators cannot delete their own accounts.")
                return

            randomPhrase = ' '.join(
                ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
                for _ in range(3)
            )

            while True:
                confirmation = input(
                    f"To confirm account deletion, please type the following phrase exactly:\n'{randomPhrase}'\nOr type 'Q' to quit: "
                ).strip()

                if confirmation == randomPhrase:
                    print("Confirmation successful. Proceeding with account deletion...")
                    break
                elif confirmation.upper() == "Q":
                    print("Exiting account deletion...")
                    return
                else:
                    print("Incorrect phrase. Please try again or type 'Q' to cancel.")
            db.deleteUserRestoreCodes(self.id,self)
            db.deleteUser(self.id,self.role)
            print("Account deleted successfully.")
            loggingSys.log("Account deleted successfully", False, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during account deletion: {str(e)}", True, username=self.userName)

    def editOwnAccount(self,db,loggingsys):
        try:
            print("======= Edit Your Account =======")
            print("You can edit your first name, last name, username, and password.")
            print("Press 'Q' at any time to quit.")

            while True:
                first_name = input(f"Enter new first name (current: ): ").strip()
                if first_name.upper() == 'Q':
                    return
                if not Validation.validateName(first_name):
                    print("Invalid first name. Please try again.")
                    loggingsys.log(f"Invalid first name during account edit: {first_name}", False, username=self.userName)
                    continue
                break

            while True:
                last_name = input(f"Enter new last name (current: ): ").strip()
                if last_name.upper() == 'Q':
                    return
                if not Validation.validateName(last_name, self.userName, loggingsys):
                    print("Invalid last name. Please try again.")
                    continue
                break

            while True:
                username = input(f"Enter new username (current: {self.userName}): ").strip()
                if username.upper() == 'Q':
                    return
                if not Validation.usernameValidation(username.lower(), self.userName, loggingsys):
                    print("Invalid username. Please try again.")
                    continue
                if db.findUsername(username.lower()):
                    print("Username already exists. Please choose another one.")
                    continue
                break


            result = db.updateUser(self.id, first_name, last_name, username.lower())
            if result == "OK":
                print("Account updated successfully.")
                loggingsys.log("Account updated", False, f"User {self.userName} updated their account.", self.userName)
            else:
                print("Failed to update account.")
                loggingsys.log("Account update failed", True, f"User {self.userName} failed to update their account.", self.userName)
        except Exception as e:
            print(f"An error occurred while editing your account: {str(e)}")
            loggingsys.log(f"Error occurred during account edit: {str(e)}", True, username=self.userName)
        
class superAdministrator(systemAdministrator):

    def generateRestoreCode(self, db,backupSys,loggingSys):
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
        
            if not backupSys.doesBackupExist(backup_name):
                return

            code = db.createRestoreCode(admin_id, backup_name,backupSys)
            if code != "FAIL":
                print(f"Restore code generated successfully: {code}")
                loggingSys.log("Restore code generated", False, f"Restore code for backup '{backup_name}' assigned to user ID {admin_id}.", self.userName)
            else:
                print("Failed to generate restore code.")
                loggingSys.log("Restore code generation failed", True, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during restore code generation: {str(e)}", True, username=self.userName)

    def manageRestoreCodes(self, db, loggingSys):
        try:
            codes = db.getAllRestoreCodes(self)
            if codes != "FAIL":
                print("======== List of Restore Codes ====================================================================================================")
                for code in codes:
                    print(f"| Code: {code[0]} | Backup File: {code[1]} | System Admin ID: {code[2]} | Creation Date: {code[3]} |\n")
                print("=============================================================================================================================")
                print("Press the id of the restore code you want to delete or press 'Q' to quit:")
                while True:
                    code_id = input().strip()
                    if code_id.upper() == "Q":
                        return
                    if code_id.isdigit():
                        code_id = int(code_id)
                        if db.deleteRestoreCode(self,code_id):
                            print(f"Restore code {code_id} deleted successfully.")
                            loggingSys.log(f"Restore code {code_id} deleted successfully.", False, username=self.userName)
                            return
                        else:
                            print("Failed to delete restore code. Please try again.")
                            loggingSys.log("Failed to delete restore code", True, username=self.userName)
                            return
                    else:
                        print("Invalid input! Please enter a valid restore code ID or 'Q' to quit.")
            else:
                print("Failed to retrieve restore codes.")
                loggingSys.log("Failed to retrieve restore codes", True, username=self.userName)
                return
        except Exception as e:
            print(f"An error occurred while retrieving restore codes: {str(e)}")
            loggingSys.log(f"Error occurred during restore code retrieval: {str(e)}", True, username=self.userName)
            return