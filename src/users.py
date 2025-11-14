from enum import Enum
from datetime import date, datetime
import os
import random
import string
import time
from database.authorization import Authorization
from cryptoUtils import CryptoUtils
from inputValidation import InputValidation
from checkSum import Checksum
from roles import roles
from userBlueprint import UserBlueprint
from utility import Utility 


class Service(UserBlueprint):

    def ChangePassword(self, db, loggingSys):
        try:
            def processChangePW():
                correctPassword = False
                while True:
                    password = input("Input your current password or press Q to quit: ")
                    if password.upper() == "Q":
                        print("Exiting...")
                        time.sleep(0.5)
                        return
                    elif InputValidation.ValidatePassword(password):
                        data = db.GetOwnUserData(self.userName,self.GetUserContext())
                        if data  != None:
                            storedPassword = data[4] 
                            storedSalt = data[8]  
                            if CryptoUtils.VerifyPassword(password, storedPassword, storedSalt):
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
                    elif InputValidation.ValidatePassword(newPassword):
                        result = db.UpdateOwnPassword(self.id, newPassword, self.GetUserContext())
                        if result == "OK":
                            self.UpdateSession(db,loggingSys)
                            print("Password has been successfully changed!")
                            loggingSys.Log("Password has been successfully changed.", False, username=self.userName)
                        else:
                            print("Failed to change password.")
                            loggingSys.Log("Failed to change password.", True, username=self.userName)
                        time.sleep(0.5)
                        return
                    else:
                        print("Please input a valid password...")

            if(db.AuthorizeAny(self.GetUserContext(),[roles.SERVICE,roles.ADMIN]) == False):
                print("You are not authorized to change password.")
                loggingSys.Log("Unauthorized access attempt to change password", True, username=self.userName)
                return
            else:
                processChangePW()

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.Log(f"Error occurred during password change: {str(e)}", True, username=self.userName)

    def EditScooter(self, db, loggingSys):
        try:
            if(db.IsAuthorized(self.GetUserContext()) == False):
                print("You are not authorized to edit scooters.")
                loggingSys.Log("Unauthorized scooter edit attempt", True, username=self.userName)
                return
            db.DisplayAllScooters(self.GetUserContext())

            while True:
                scooter_id = input("Enter the ID of the scooter you want to edit (or 'Q' to quit): ")
                if scooter_id.upper() == 'Q':
                    return
                if not InputValidation.ValidateNumericInput(scooter_id):
                    print("Invalid ID format.")
                    continue

                scooter_data = db.GetScooterById(scooter_id,self.GetUserContext())
                if scooter_data:
                    
                    break
                else:
                    print("Scooter ID not found.")

            editable_fields = {
                "brand":               InputValidation.ValidateBrandOrModel,
                "model":               InputValidation.ValidateBrandOrModel,
                "serial_number":       InputValidation.ValidateSerialNumber,
                "top_speed":           lambda v: Utility.ValidateIntegerInRange(v, "5", "120"),
                "battery_capacity":    lambda v: Utility.ValidateIntegerInRange(v, "100", "2000"),
                "state_of_charge":     lambda v: Utility.ValidateIntegerInRange(v, "0", "100"),
                "target_soc_min":      lambda v: Utility.ValidateIntegerInRange(v, "0", "100"),
                "target_soc_max":      lambda v: Utility.ValidateIntegerInRange(v, "0", "100"),
                "mileage":             lambda v: Utility.ValidateIntegerInRange(v, "0", "999999"),
                "last_maintenance_date":Utility.ValidateDate,
                "latitude":            Utility.ValidateLatitude,
                "longitude":           Utility.ValidateLongtitude,
                "out_of_service":          InputValidation.ValidateStatus
            }

            if self.role == roles.SERVICE:
                allowed = {
                    "state_of_charge", "target_soc_min", "target_soc_max",
                    "mileage", "last_maintenance_date", "out_of_service"
                }
            else:
                allowed = set(editable_fields.keys())

            updates = {}
            for field, validator in editable_fields.items():
                if field not in allowed:
                    continue
                current_val = scooter_data.get(field, "")
                new_val = Utility.GetOptionalUpdate(
                    f"Update {field.replace('_', ' ').title()}",
                    validator,
                    current_val,
                    self.userName,
                    loggingSys=loggingSys,
                    fieldName=field
                )
                if new_val == "Q":
                    print("Cancelled editing.")
                    return
                if new_val != current_val:
                    updates[field] = new_val

            if not updates:
                print("No changes were made.")
                return

            if db.updateScooter(scooter_id, updates,self.GetUserContext()) == "OK":
                print("Scooter updated successfully.")
                loggingSys.Log(
                    "Scooter edited",
                    False,
                    f"Scooter ID {scooter_id} edited fields: {', '.join(updates.keys())}",
                    self.userName
                )
            else:
                print("Failed to update scooter.")
                loggingSys.Log(
                    "Scooter edit failed",
                    True,
                    f"Scooter ID {scooter_id} update failed.",
                    self.userName
                )

        except Exception as e:
            print(f"An error occurred while editing scooter: {e}")
            loggingSys.Log(
                "Error occurred during scooter editing",
                True,
                str(e),
                username=self.userName
            )

    def SearchScooter(self, db, loggingSys):
        try:
            if(db.IsAuthorized(self.GetUserContext()) == False):
                print("You are not authorized to search scooters.")
                loggingSys.Log("Unauthorized scooter search attempt", True, username=self.userName)
                return
            search_term = input("Enter the search key: ")
            if not InputValidation.DetectBadInput(search_term) and len(search_term) <= 35:
                result = db.SearchScooter(search_term,self.GetUserContext())
            
                if result:
                    print("Search Results:")
                    print("----------------")
                    for row in result:
                        print(f"Scooter ID: {row[0]} | In Service Date: {row[1]} | Brand: {row[2]} | Model: {row[3]} | Serial Number: {row[4]} | Top Speed: {row[5]} km/h | Battery Capacity: {row[6]} Wh | State of Charge: {row[7]}% | Target SOC Min: {row[8]}% | Target SOC Max: {row[9]}% | Latitude: {row[10]} | Longitude: {row[11]} | Out of service: {row[12]} | Mileage: {row[13]} km | Last Maintenance Date: {row[14]}")
                        print("----------------")
                else:
                    print("No results found.")
            
                input("Press any key to continue...")
            else:
                print("Invalid search key")
                return

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.Log(f"Error occurred during scooter search: {str(e)}", True, username=self.userName)

class SystemAdministrator(Service):

    def SearchTraveller(self, db, loggingSys):
        try:
            if(db.AuthorizeTavellerManagement(self.GetUserContext()) == False):
                print("You are not authorized to create travellers.")
                loggingSys.Log("Unauthorized traveller creation attempt", True, username=self.userName)
                return
            search_term = input("Enter the search key: ")
            if not InputValidation.DetectBadInput(search_term) and len(search_term) <= 35:
                result = db.SearchTraveller(search_term,self.GetUserContext())
            
                if result:
                    print("Search Results:")
                    print("----------------")
                    for row in result:
                        print(f"Customer ID: {row[0]} | Registration Date: {row[1]} | First Name: {row[2]} | Last Name: {row[3]} | Birthdate: {row[4]} | Gender: {row[5]} | Street: {row[6]} | House Number: {row[7]} | City: {row[8]} | Zip Code: {row[9]} | Email: {row[10]} | Mobile: {row[11]} | License Number: {row[12]}")
                        print("----------------")
                else:
                    print("No results found.")
            
                input("Press any key to continue...")
            else:
                print("Invalid search key")
                return

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.Log(f"Error occurred during scooter search: {str(e)}", True, username=self.userName)

    def DeleteTraveller(self, db, loggingSys):
        try:
            if(db.AuthorizeTavellerManagement(self.GetUserContext()) == False):
                print("You are not authorized to create travellers.")
                loggingSys.Log("Unauthorized traveller creation attempt", True, username=self.userName)
                return
            db.DisplayAllTravellers(self.GetUserContext())

            while True:
                traveller_id = input("Enter the ID of the scooter you want to edit or press 'Q' to quit: ")
                if traveller_id.upper() == 'Q':
                    return
                if not InputValidation.ValidateMembershipID(traveller_id):
                    print("Invalid ID format.")
                    loggingSys.Log("Invalid ID format entered for traveller deletion", True,f"Input: {traveller_id}" ,username=self.userName)
                    continue

                traveller_id = int(traveller_id)
                if traveller_id:
                    break
                else:
                    print("Scooter ID not found.")
            
            if db.DeleteTraveller(traveller_id, self,self.GetUserContext())  == "OK":
                print("Traveller deleted successfully.")
                loggingSys.Log("Traveller deleted", False, f"Traveller ID {traveller_id} deleted.", self.userName)
            else:
                print("Failed to delete traveller.")
                loggingSys.Log("Traveller deletion failed", True, f"Traveller ID {traveller_id} deletion failed.", self.userName)
        except Exception as e:
            print(f"An error occurred while deleting traveller: {str(e)}")
            loggingSys.Log(f"Error occurred during traveller deletion: {str(e)}", True, username=self.userName)

    def DeleteScooter(self, db, loggingSys):
        try:
            if(db.AuthorizeAny(self.GetUserContext(),[roles.SUPERADMIN,roles.ADMIN]) == False):
                print("You are not authorized to delete scooters.")
                loggingSys.Log("Unauthorized scooter deletion attempt", True, username=self.userName)
                return
            db.DisplayAllScooters(self.GetUserContext())

            while True:
                scooter_id = input("Enter the ID of the scooter you want to edit or press 'Q' to quit: ")
                if scooter_id.upper() == 'Q':
                    return
                if not InputValidation.ValidateNumericInput(scooter_id):
                    print("Invalid ID format.")
                    continue

                scooter_id = int(scooter_id)
                if db.GetScooterById(scooter_id,self.GetUserContext()):
                    break
                else:
                    print("Scooter ID not found.")
            
            if db.DeleteScooter(scooter_id, self,self.GetUserContext())  == "OK":
                print("Scooter deleted successfully.")
                loggingSys.Log("Scooter deleted", False, f"scooter ID {scooter_id} deleted.", self.userName)
            else:
                print("Failed to delete scooter.")
                loggingSys.Log("Scooter deletion failed", True, f"Scooter ID {scooter_id} deletion failed.", self.userName)
        except Exception as e:
            print(f"An error occurred while deleting scooter: {str(e)}")
            loggingSys.Log(f"Error occurred during Scooter deletion: {str(e)}", True, username=self.userName)

    def Deletion(self, db, role, loggingSys):
        try:
            def processDeletion(role):
                self.DisplayUsers(db, role)
                roleType = role.value

                validID = False
                while True:
                    Id = input(f"Enter the ID of the {roleType} you would like to delete or enter 'Q' to quit: ")
                    if Id.upper() == "Q":
                        return

                    if not InputValidation.ValidateNumericInput(Id):
                        print("ID is invalid!")
                        time.sleep(0.5)
                        continue

                    Id = int(Id)
                    if db.FindUserID(Id, role):
                        validID = True
                        break
                    else:
                        print("ID not found in the database!")
                        time.sleep(0.5)

                if validID:
                    deletedUsername = db.GetUsernameByID(Id)
                    db.DeleteUserRestoreCodes(Id,self,self.GetUserContext())
                    result = db.DeleteUser(Id, role,self.GetUserContext())
                    if result == "OK":
                        print("User deleted.")
                        loggingSys.Log("User deleted", False, f"User '{deletedUsername}' has been deleted.", self.userName)
                    else:
                        print("An error occurred while deleting the user.")
                        loggingSys.Log("Failed to delete user", True, f"An error occurred while deleting the user: {deletedUsername}.", self.userName)
                    time.sleep(1)

            if (db.AuthorizeUserManagement(self.GetUserContext(), role)):
                processDeletion(role)
            else:
                print("You are not authorized to reset passwords for other users.")
                loggingSys.Log("Unauthorized access attempt to reset password", True, username=self.userName)
                return 

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.Log(f"Error occurred during deletion: {str(e)}", True, username=self.userName)

    def CreateTraveller(self, db, role, loggingSys):
        try:
            if(db.AuthorizeTavellerManagement(self.GetUserContext()) == False):
                print("You are not authorized to create travellers.")
                loggingSys.Log("Unauthorized traveller creation attempt", True, username=self.userName)
                return
            print("========== Traveller Registration ==========")
            traveller = {}

            def ask(field, prompt, validator):
                val = Utility.GetValidInput(prompt, validator, self.userName, loggingSys, field)
                if val == None:
                    print("Cancelled input. Exiting registration.")
                    raise KeyboardInterrupt
                return val

            traveller["first_name"] = ask("First Name", "Enter traveller's first name: ", InputValidation.ValidateName)
            traveller["last_name"] = ask("Last Name", "Enter traveller's last name: ", InputValidation.ValidateName)
            traveller["birthdate"] = ask("Birthdate","Enter traveller's birthdate: ",Utility.ValidateDate)
            traveller["gender"] = ask("Gender", "Enter traveller's gender (male/female/other): ",InputValidation.ValidateGender)
            traveller["street"] = ask("Street","Enter traveller's street name: ",InputValidation.ValidateAddress)
            traveller["house_number"] = ask("House number","Enter traveller's house number: ",InputValidation.ValidateHousenumber)
            traveller["city"] = ask("City","Enter traveller's city: ",InputValidation.ValidateCity)
            traveller["zip_code"] = ask("Zipcode","Enter traveller's zipcode: ",InputValidation.ValidateZipcode)
            traveller["email"] = ask("Email","Enter traveller's email",InputValidation.ValidateEmailAddress)
            traveller["mobile"] = ask("Mobile number","Enter traveller's mobile number : +316-",InputValidation.ValidateMobileNumber)
            traveller["license_number"] = ask("License number","Enter traveller's license number: ",InputValidation.ValidateDrivingLicense)
            traveller["registration_date"] = date.today().strftime("%Y-%m-%d")
            traveller["customer_id"] = Checksum.GenerateTravellerID(db)

            result = db.CreateTraveller(traveller,self.GetUserContext())

            if result == "OK":
                print("Traveller registered successfully.")
                loggingSys.Log("Traveller registered", False, f"Traveller with ID {traveller['customer_id']} registered.", self.userName)
            else:
                print("Failed to register traveller.")
                loggingSys.Log("Failed to register traveller", True, username=self.userName)

        except KeyboardInterrupt:
            print("Traveller registration was cancelled.")
            loggingSys.Log("Traveller registration cancelled by user", False, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.Log(f"Exception during traveller registration: {str(e)}", True, username=self.userName)

    def CreateScooter(self, db, loggingSys):
        try:
            if(db.AuthorizeAny(self.GetUserContext(),[roles.SUPERADMIN,roles.ADMIN]) == False):
                print("You are not authorized to create scooters.")
                loggingSys.Log("Unauthorized scooter creation attempt", True, username=self.userName)
                return
            print("========== Scooter Registration ==========")
            scooter = {}

            def ask(field, prompt, validator):
                val = Utility.GetValidInput(prompt, validator, self.userName, loggingSys, field)
                if val is None:
                    print("Cancelled input. Exiting registration.")
                    raise KeyboardInterrupt
                return val

            scooter["serial_number"] = ask("Serial Number", "Enter serial number:", InputValidation.ValidateSerialNumber)
            scooter["brand"] = ask("Brand", "Enter scooter brand:", InputValidation.ValidateBrandOrModel)
            scooter["model"] = ask("Model", "Enter scooter model:", InputValidation.ValidateBrandOrModel)
            scooter["top_speed"] = ask("Top Speed", "Enter top speed (km/h):", lambda v: Utility.ValidateIntegerInRange(v, "5", "120"))
            scooter["battery_capacity"] = ask("Battery Capacity", "Enter battery capacity (Wh):", lambda v: Utility.ValidateIntegerInRange(v, "100", "2000"))
            scooter["state_of_charge"] = ask("State of Charge", "Enter current charge (0-100):", lambda v: Utility.ValidateIntegerInRange(v, "0", "100"))
            scooter["target_soc_min"] = ask("Target SOC Min", "Enter minimum charge threshold (0-100):", lambda v: Utility.ValidateIntegerInRange(v, "0", "100"))
            scooter["target_soc_max"] = ask("Target SOC Max", f'Enter maximum charge threshold ({scooter["target_soc_min"]}-100):', lambda v: Utility.ValidateIntegerInRange(v, scooter["target_soc_min"], "100"))
            scooter["mileage"] = ask("Mileage", "Enter current mileage (default 0):", lambda v: Utility.ValidateIntegerInRange(v, "0", "999999"))
            scooter["latitude"] = ask("Latitude", "Enter scooter latitude (e.g. 51.92250):", Utility.ValidateLatitude)
            scooter["longitude"] = ask("Longitude", "Enter scooter longitude (e.g. 4.47917):", Utility.ValidateLongtitude)

            scooter["in_service_date"] = datetime.today().strftime("%Y-%m-%d")
            scooter["last_maintenance_date"] = scooter["in_service_date"]

            result = db.CreateScooter(scooter,self.GetUserContext())

            if result == "OK":
                print("Scooter registered successfully.")
                loggingSys.Log("Scooter registered", False, f"Serial: {scooter['serial_number']}", self.userName)
            else:
                print("Failed to register scooter.")
                loggingSys.Log("Scooter registration failed", True, username=self.userName)

        except KeyboardInterrupt:
            print("Scooter registration was cancelled.")
            loggingSys.Log("Scooter registration cancelled by user", False, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {e}")
            loggingSys.Log(f"Scooter creation error: {str(e)}", True, username=self.userName)

    def CreateBackup(self,db ,backUpSystem, loggingSys):
        try:
            if(db.AuthorizeAny(self.GetUserContext(),[roles.ADMIN,roles.SUPERADMIN]) == False):
                print("You are not authorized to create backups.")
                loggingSys.Log("Unauthorized backup creation attempt", True, username=self.userName)
                time.sleep(0.5)
                return
            while True:
                keyPress = input("Would you like to create a back up [Y/N] ")
                if keyPress.upper() == "Y":
                    print("Creating backup....")
                    backUpSystem.CreateBackupZip(self)
                    time.sleep(5)
                    break
                elif keyPress.upper() == "N":
                    print("Exiting.....")
                    break
                else:
                    print("Invalid input...")

        except Exception as e:
            print(f"An error occurred while creating backup: {str(e)}")
            loggingSys.Log(f"Error occurred during backup creation: {str(e)}", True, username=self.userName)

    def UserCreation(self, db, role, loggingSys):
        try:
            if (db.AuthorizeUserManagement(self.GetUserContext(), role)) == False:
                print("Invalid role")
                loggingSys.Log("User tried to create a user with an invalid RoleType", True, username=self.userName)
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
                    if not InputValidation.ValidateName(firstName):
                        print("Please enter a valid firstname!!!")
                        loggingSys.Log(f"User tried to create a {roleType} with either an invalid first name or last name", False, username=self.userName)
                        continue
                    else:
                        validF_Name = True

                while not validL_Name:
                    lastName = input(f"Enter the last name of the new {roleType} or press Q to quit...\n")
                    if lastName.upper() == 'Q':
                        return
                    if not InputValidation.ValidateName(lastName):
                        print("Please enter a valid lastname!!!")
                        loggingSys.Log(f"User tried to create a {roleType} with either an invalid first name or last name", False, username=self.userName)
                        continue
                    else:
                        validL_Name = True

                while not availableUsername:
                    username = input(f"Enter the username of the new {roleType} or press Q to quit...\n")
                    if username.upper() == 'Q':
                        return
                    if not InputValidation.ValidateUsername(username):
                        print("Please insert a valid username...")
                        loggingSys.Log(f"User tried to create a {roleType} with an invalid username", False, username=self.userName)
                        continue
                    if db.FindUsername(username.lower()):
                        print("Username already exists...")
                        loggingSys.Log(f"User tried to create a {roleType} with an existing username", False, username=self.userName)
                    else:
                        print("Username is available!")
                        availableUsername = True

                while not validPassword:
                    password = input(f"Enter the password of the new {roleType} or press Q to quit...\n")
                    if password.upper() == 'Q':
                        return
                    if not InputValidation.ValidatePassword(password):
                        print("Please enter a valid password!!!")
                        loggingSys.Log(f"User tried to create a {roleType}: with an invalid password", False, username=self.userName)
                        continue
                    else:
                        validPassword = True
                        break

                creationDate = date.today().strftime("%Y-%m-%d")
                result = db.CreateUser(firstName, lastName, username, password, creationDate, role, False,self.GetUserContext())
                if result == "OK":
                    print(f"{roleType} created successfully.")
                    loggingSys.Log(f"User has created a {roleType}", False, username=self.userName)
                else:
                    print(f"Failed to create {roleType}.")
                    loggingSys.Log(f"Failed to create {roleType}", True, username=self.userName)
        except Exception as e:
            print(f"An error occurred while creating user: {str(e)}")
            loggingSys.Log(f"Error occurred during user creation: {str(e)}", True, username=self.userName)

        processCreation()

    def DisplayUsers(self, db, role=None):
        try:
            userContext = self.GetUserContext()
            if(db.AuthorizeAny(userContext, [roles.SUPERADMIN,roles.ADMIN]) == False):
                print("You are not authorized to view users of this role.")
            allUsers = db.GetUsers(userContext,role)
            title = "user" if role is None else f"{role.value}"
            print(f"======== List of {title}s ====================================================================================================")
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
    
    def DisplayLogs(self, db ,loggingSys):
        try:
            if(db.AuthorizeAny(self.GetUserContext(),[roles.ADMIN,roles.SUPERADMIN]) == False):
                print("You are not authorized to view logs.")
                loggingSys.Log("Unauthorized log viewing attempt", True, username=self.userName)
                return
            print("====================Unique Meal Logs====================\n")
            loggingSys.PrintLogs()
            print("Press any key to continue...")
            keyPress = input()
        except Exception as e:
            print(f"An error occurred while displaying logs: {str(e)}")
            loggingSys.Log(f"Error occurred during display logs: {str(e)}", True, username=self.userName)

    def AlertLogs(self, loggingSys):
        try:
            if loggingSys.HasUncheckedSuspiciousLogs():
                print("There are new suspicious activities that havent been checked \nGo check the logs as soon as possible!!!")
            else:
                print("No new suspicious activities logged...")
        except Exception as e:
            print(f"An error occurred while sending log alert: {str(e)}")
            loggingSys.Log(f"Error occurred during log alert: {str(e)}", True, username=self.userName)

    def EditTraveller(self, db, loggingSys):
        try:
            if(db.AuthorizeTavellerManagement(self.GetUserContext()) == False):
                print("You are not authorized to create travellers.")
                loggingSys.Log("Unauthorized traveller creation attempt", True, username=self.userName)
                return
            db.DisplayAllTravellers(self.GetUserContext())
            while True:
                traveller_id = input("Enter the ID of the traveller you want to edit (or Q to quit): ")
                if traveller_id.upper() == 'Q':
                    return
                if not InputValidation.ValidateMembershipID(traveller_id):
                    print("Invalid ID")
                    continue
                traveller_data = db.GetTravellerById(traveller_id,self.GetUserContext())
                if traveller_data:
                    break
                print("Traveller ID not found.")

            print("\nCurrent traveller data:")
            for field, val in traveller_data.items():
                print(f"  {field.replace('_', ' ').title()}: {val}")
            print()

            editable_fields = {
                "first_name":     InputValidation.ValidateName,
                "last_name":      InputValidation.ValidateName,
                "birthday":       Utility.ValidateDate,
                "gender":         InputValidation.ValidateGender,
                "street_name":    InputValidation.ValidateAddress,
                "house_number":   InputValidation.ValidateHousenumber,
                "city":           InputValidation.ValidateCity,
                "zip_code":       InputValidation.ValidateZipcode,
                "email":          InputValidation.ValidateEmailAddress,
                "mobile":         InputValidation.ValidateMobileNumber,
                "license_number": InputValidation.ValidateDrivingLicense,
            }

            updates = {}
            for field, validator in editable_fields.items():
                current = traveller_data.get(field, "")
                new_val = Utility.GetOptionalUpdate(
                    f"Update {field.replace('_', ' ').title()}",
                    validator,
                    current,
                    self.userName,
                    loggingSys,
                    fieldName=field
                )
                if new_val == "Q":
                    print("Cancelled editing.")
                    return
                if new_val != current:
                    updates[field] = new_val

            if not updates:
                print("No changes were made.")
                return

            if db.UpdateTraveller(traveller_id, updates,self.GetUserContext()) == "OK":
                print("Traveller updated successfully.")
                loggingSys.Log(
                    "Traveller edited",
                    False,
                    f"Traveller ID {traveller_id} edited fields: {', '.join(updates.keys())}.",
                    self.userName
                )
            else:
                print("Failed to update traveller.")
                loggingSys.Log(
                    "Traveller edit failed",
                    True,
                    f"Traveller ID {traveller_id} update failed.",
                    self.userName
                )

        except Exception as e:
            print(f"An error occurred while editing traveller: {e}")
            loggingSys.Log(
                "Error during traveller editing",
                True,
                str(e),
                username=self.userName
            )

    def EditUser(self, db, role, loggingSys):
        try:
            def processEdit(role):
                self.DisplayUsers(db, role)
                validID = False
                userID = ""
                while True:
                    userID = input(f"Enter the ID of the {role.value} you would like to edit or enter 'Q' to quit: ")
                    if userID.upper() == "Q":
                        return
                    elif InputValidation.ValidateNumericInput(userID):
                        if db.FindUserID(int(userID), role):
                            validID = True
                            break
                    else:
                        print("ID not found in the database!" if InputValidation.ValidateNumericInput(userID) else "ID is invalid!")
                        time.sleep(0.5)

                if validID:
                    while True:
                        firstName = input(f"Enter the new first name for user or press 'Q' to quit: ")
                        if firstName.upper() == 'Q':
                            return
                        if not InputValidation.ValidateName(firstName):
                            print("Invalid first name!")
                        else:
                            break

                    while True:
                        lastName = input(f"Enter the new last name for user or press 'Q' to quit: ")
                        if lastName.upper() == 'Q':
                            return
                        if not InputValidation.ValidateName(lastName):
                            print("Invalid last name!")
                        else:
                            break

                    while True:
                        username = input(f"Enter the new username for user or press 'Q' to quit: ")
                        if username.upper() == 'Q':
                            return
                        if not InputValidation.ValidateUsername(username.lower()):
                            print("Invalid username!")
                        elif db.FindUsername(username.lower()):
                            print("Username already exists!")
                        else:
                            break
                    result = db.UpdateUser(userID, firstName, lastName, username.lower(),self.GetUserContext(),role)
                    if result == "OK":
                        print("User information updated successfully.")
                    else:
                        print("Failed to update user information.")

            if (db.AuthorizeUserManagement(self.GetUserContext(), role)):
                processEdit(role)
            else:
                print("You are not authorized to reset passwords for other users.")
                loggingSys.Log("Unauthorized access attempt to reset password", True, username=self.userName)
                return 

        except Exception as e:
            print(f"An error occurred while editing user: {str(e)}")
            loggingSys.Log(f"Error occurred during user edit: {str(e)}", True, username=self.userName)
    
    def ResetPassword(self, db, role, loggingSys):
        try:
            def processReset(role):
                self.DisplayUsers(db, role)
                validID = False
                userID = ""
                
                while True:
                    userID = input(f"Enter the ID of the {role.value} you would like to edit or enter 'Q' to quit: ")
                    
                    if userID.upper() == "Q":
                        return
                    elif InputValidation.ValidateNumericInput(userID):
                        if db.FindUserID(int(userID), role):
                            validID = True
                            break
                    else:
                        print("ID not found in the database!" if InputValidation.ValidateNumericInput(userID) else "ID is invalid!")
                        time.sleep(0.5)
                
                if validID:
                    while True:
                        password = input("Enter the new temporary password for the user or press Q to quit: ")
                        
                        if password.upper() == "Q":
                            print("Exiting...")
                            time.sleep(0.5)
                            return
                        elif InputValidation.ValidatePassword(password):
                            result = db.UpdatePassword(userID, password,self.GetUserContext(),role ,True)
                            
                            if result == "OK":
                                print("Password updated successfully.")
                                loggingSys.Log("Password successfully reset", False, username=userID)
                                return
                            else:
                                print("Failed to update password.")
                                loggingSys.Log("Password reset failed", True, username=userID)
                        else:
                            print("Please enter a valid password!")
            
            if (db.AuthorizeUserManagement(self.GetUserContext(), role)):
                processReset(role)
            else:
                print("You are not authorized to reset passwords for other users.")
                loggingSys.Log("Unauthorized access attempt to reset password", True, username=self.userName)
                return 
        except Exception as e:
            print(f"An error occurred while resetting password: {str(e)}")
            loggingSys.Log(f"Error occurred during password reset: {str(e)}", True, username=self.userName)

    def RestoreBackup(self, backUpSystem, loggingSys,db):
        try:
            if(db.AuthorizeAny(self.GetUserContext(),[roles.ADMIN,roles.SUPERADMIN]) == False):
                print("You are not authorized to restore backups.")
                loggingSys.Log("Unauthorized backup restoration attempt", True, username=self.userName)
                return
            backUpSystem.ListBackupNames()
            if(self.role == roles.SUPERADMIN):
                while True:
                    name = input("Enter the name of the backup file to restore or press Q to quit: ")
                    if name.upper() == "Q":
                        print("Quitting...")
                        break

                    if not InputValidation.ValidateBackup(name):
                        print("Please enter a valid backup filename!")
                        continue

                    print("Restoring backup as Super Administrator...")
                    backUpSystem.RestoreBackup(name, username=self.userName)
                    db.ClearAllSessions()
                    break
                return
            elif(self.role == roles.ADMIN):
                codes = db.GetRestoreCodesByUser(self.id,self.GetUserContext())
                if not codes:
                    print("No restore codes found for your account.")
                    return

                print("\nYour restore codes:")
                for code, filename in codes:
                    print(f"- Code: {code} | Backup: {filename}")
                print()

                while True:
                    name = input("Enter the name of the backup file to restore or press Q to quit: ")
                    if name.upper() == "Q":
                        print("Quitting...")
                        break

                    if not InputValidation.ValidateBackup(name):
                        print("Please enter a valid backup filename!")
                        continue

                    code = input("Enter your restore code or press Q to quit: ")
                    if code.upper() == "Q":
                        print("Quitting...")
                        break

                    if (code, name) in codes:
                        print("Restore code valid. Restoring backup...")
                        db.DeleteUserRestoreCodes( self.id, self, self.GetUserContext())
                        backUpSystem.RestoreBackup(name, username=self.userName)
                        break
                    else:
                        print("Invalid restore code or backup mismatch.")

            else:
                print("Unauthorized user type. You are not allowed to restore backups.")

        except Exception as e:
            print(f"An error occurred while restoring backup: {str(e)}")
            loggingSys.Log(f"Error occurred during backup restoration: {str(e)}", True, username=self.userName)

    def AccountDeletion(self,db, loggingSys):
        try:
            if(db.AuthorizeAction(self.GetUserContext(), roles.ADMIN) == False):
                print("You are not authorized to delete your account.")
                loggingSys.Log("Unauthorized account deletion attempt", True, username=self.userName)
                return

            randomPhrase = ' '.join(
                ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
                for _ in range(3)
            )

            while True:
                confirmation = input(f"To confirm account deletion, please type the following phrase exactly:\n'{randomPhrase}'\nOr type 'Q' to quit: ")

                if confirmation == randomPhrase:
                    print("Confirmation successful. Proceeding with account deletion...")
                    break
                elif confirmation.upper() == "Q":
                    print("Exiting account deletion...")
                    return
                else:
                    print("Incorrect phrase. Please try again or type 'Q' to cancel.")
            db.DeleteUserRestoreCodes(self.id,self,self.GetUserContext())
            db.DeleteUser(self.id,self.role,self.GetUserContext())
            print("Account deleted successfully.")
            loggingSys.Log("Account deleted successfully", False, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.Log(f"Error occurred during account deletion: {str(e)}", True, username=self.userName)

    def EditOwnAccount(self,db,loggingsys):
        try:
            if(db.AuthorizeAction(self.GetUserContext(), roles.ADMIN) == False):
                print("You are not authorized to edit your account.")
                loggingsys.Log("Unauthorized account edit attempt", True, username=self.userName)
                return
            print("======= Edit Your Account =======")
            print("You can edit your first name, last name, username, and password.")
            print("Press 'Q' at any time to quit.")

            while True:
                first_name = input(f"Enter new first name (current: ): ")
                if first_name.upper() == 'Q':
                    return
                if not InputValidation.ValidateName(first_name):
                    print("Invalid first name. Please try again.")
                    loggingsys.Log(f"Invalid first name during account edit: {first_name}", False, username=self.userName)
                    continue
                break

            while True:
                last_name = input(f"Enter new last name (current: ): ")
                if last_name.upper() == 'Q':
                    return
                if not InputValidation.ValidateName(last_name):
                    print("Invalid last name. Please try again.")
                    continue
                break

            while True:
                username = input(f"Enter new username (current: {self.userName}): ")
                if username.upper() == 'Q':
                    return
                if not InputValidation.ValidateUsername(username.lower()):
                    print("Invalid username. Please try again.")
                    continue
                if db.FindUsername(username.lower()):
                    print("Username already exists. Please choose another one.")
                    continue
                break


            result = db.UpdateSelf(self.id, first_name, last_name, username.lower(),self.GetUserContext())
            if result == "OK":
                self.UpdateSession(db,loggingsys)
                print("Account updated successfully.")
                loggingsys.Log("Account updated", False, f"User {self.userName} updated their account.", self.userName)
                self._userName = username.lower()
            else:
                print("Failed to update account.")
                loggingsys.Log("Account update failed", True, f"User {self.userName} failed to update their account.", self.userName)
        except Exception as e:
            print(f"An error occurred while editing your account: {str(e)}")
            loggingsys.Log(f"Error occurred during account edit: {str(e)}", True, username=self.userName)
        
class SuperAdministrator(SystemAdministrator):

    def GenerateRestoreCode(self, db,backupSys,loggingSys):
        try:
            if(db.AuthorizeAction(self.GetUserContext(), roles.SUPERADMIN) == False):
                print("You are not authorized to generate restore codes.")
                loggingSys.Log("Unauthorized restore code generation attempt", True, username=self.userName)
                return
            backupSys.ListBackupNames()
            self.DisplayUsers(db, roles.ADMIN)

            while True:
                admin_id = input("Enter the ID of the System Administrator to generate a restore code for, or press Q to quit: ")
                if admin_id.upper() == "Q":
                    return
                if InputValidation.ValidateNumericInput(admin_id) and db.FindUserID(int(admin_id), roles.ADMIN):
                    admin_id = int(admin_id)
                    break
                else:
                    print("Invalid ID or not a System Administrator!")
                    time.sleep(0.5)

            backup_name = input("Enter the exact name of the backup file (e.g., backup_20240601_1700.zip) or press Q to quit: ")
            if backup_name.upper() == "Q":
                return
        
            if not backupSys.DoesBackupExist(backup_name):
                return

            code = db.CreateRestoreCode(admin_id, backup_name,backupSys,self.GetUserContext())
            if code != "FAIL":
                print(f"Restore code generated successfully: {code}")
                loggingSys.Log("Restore code generated", False, f"Restore code for backup '{backup_name}' assigned to user ID {admin_id}.", self.userName)
            else:
                print("Failed to generate restore code.")
                loggingSys.Log("Restore code generation failed", True, username=self.userName)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.Log(f"Error occurred during restore code generation: {str(e)}", True, username=self.userName)

    def ManageRestoreCodes(self, db, loggingSys):
        try:
            if(db.AuthorizeAction(self.GetUserContext(), roles.SUPERADMIN) == False):
                print("You are not authorized to generate restore codes.")
                loggingSys.Log("Unauthorized restore code generation attempt", True, username=self.userName)
                return
            codes = db.GetAllRestoreCodes(self,self.GetUserContext())
            if codes != "FAIL":
                print("======== List of Restore Codes ====================================================================================================")
                for code in codes:
                    print(f"| ID: {code[0]} | System Admin ID: {code[1]} | Code: {Utility.SafeDecrypt(code[2])} | Backup File: {code[3]} |\n")
                print("=============================================================================================================================")
                print("Press the id of the restore code you want to delete or press 'Q' to quit:")
                while True:
                    code_id = input()
                    if code_id.upper() == "Q":
                        return
                    if code_id.isdigit():
                        code_id = int(code_id)
                        if db.DeleteRestoreCode(self,code_id,self.GetUserContext()) != "FAIL":
                            print(f"Restore code {code_id} deleted successfully.")
                            loggingSys.Log(f"Restore code {code_id} deleted successfully.", False, username=self.userName)
                            return
                        else:
                            print("Failed to delete restore code. Please try again.")
                            loggingSys.Log("Failed to delete restore code", True, username=self.userName)
                            return
                    else:
                        print("Invalid input! Please enter a valid restore code ID or 'Q' to quit.")
            else:
                print("Failed to retrieve restore codes.")
                loggingSys.Log("Failed to retrieve restore codes", True, username=self.userName)
                return
        except Exception as e:
            print(f"An error occurred while retrieving restore codes: {str(e)}")
            loggingSys.Log(f"Error occurred during restore code retrieval: {str(e)}", True, username=self.userName)
            return