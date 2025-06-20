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

#     def memberCreation(self, db, loggingSys):
#         try:
#             print("""
# 1. Email Validation:
#    - Must be in a valid email format (`username@domain.com`).

# 2. Age Validation:
#    - Must be an integer between 1 and 100.

# 3. House Number Validation:
#    - Must be an integer between 1 and 9999.

# 4. Zip Code Validation:
#    Must be a valid Dutch zip code format for example 1234AB.

# 5. Name Validation:
#    - Must contain only alphabetic characters, hyphens, apostrophes.
#    - Maximum of one hyphen or apostrophe, and two spaces.
#    - Cannot start or end with a hyphen or apostrophe.
#    - Cannot be empty.

# 6. Mobile Number Validation:
#    - Must be a valid dutch number for example +31622222222.

# 8. Address Validation:
#     - Must contain only alphanumeric characters, spaces, dots, commas, apostrophes, hyphens, or single quotes.
#     - Cannot be empty.

# 9. City Validation:
#     - Must be one of the following cities: Amsterdam, Rotterdam, The Hague, Utrecht, Eindhoven, Tilburg, Groningen, Almere, Breda, Nijmegen.
# """)

#             public_key = cryptoUtils.loadPublicKey()
#             firstName = ""
#             while not firstName:
#                 firstName = input("Enter the member's first name or press 'Q' to quit: ").strip()
#                 if firstName.upper() == 'Q':
#                     return
#                 if not Validation.validateName(firstName, self.userName, loggingSys):
#                     print("Invalid firstName!")
#                     firstName = ""

#             lastName = ""
#             while not lastName:
#                 lastName = input("Enter the member's lastName or press 'Q' to quit: ").strip()
#                 if lastName.upper() == 'Q':
#                     return
#                 if not Validation.validateName(lastName, self.userName, loggingSys):
#                     print("Invalid lastName!")
#                     lastName = ""

#             age = ""
#             while not age:
#                 age = input("Enter the member's age or press 'Q' to quit: ").strip()
#                 if age.upper() == 'Q':
#                     return
#                 if not Validation.validateAge(age, self.userName, loggingSys):
#                     print("Invalid age!")
#                     age = ""

#             gender = ""
#             while not gender:
#            elif isinstance(user, service):
#                role = roles.SERVICE
#                     return
#                 if gender not in ['Male', 'Female', 'Other']:
#                     print("Invalid gender!")
#                     gender = ""

#             weight = ""
#             while not weight:
#                 weight = input("Enter the member's weight or press 'Q' to quit: ").strip()

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
            print(f"An error occurred while editing scooter: {str(e)}")
            loggingSys.log(f"Error occurred during scooter editing: {str(e)}", True, username=self.userName)

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

    def deletion(self, user, db, role, loggingSys):
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
                        loggingSys.log("User deleted", False, f"User '{deletedUsername.decode('utf-8')}' has been deleted.", self.userName)
                    else:
                        print("An error occurred while deleting the user.")
                        loggingSys.log("Failed to delete user", True, f"An error occurred while deleting the user: {deletedUsername.decode('utf-8')}.", self.userName)
                    time.sleep(1)
#             else:
            if isinstance(user, superAdministrator):
                if role in [roles.ADMIN, roles.SERVICE]:
                    processDeletion(role)
                else:
                    print("Invalid request...")
            elif isinstance(user, systemAdministrator):
                if role == roles.SERVICE:
                    processDeletion(role)
                else:
                    print("Unauthorized request.")
            elif isinstance(user, service):
                print("You are not authorized to delete any users.")
            else:
                print("Unauthorized access...")
        except Exception as e:
            print(f"An error occurred during scooter update:", e)
            loggingSys.log(f"Error occurred during scooter update: {str(e)}", True, username=self.userName)
            return
#                 print("An error occurred while registering the member.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during deletion: {str(e)}", True, username=self.userName)
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             loggingSys.log("Unsuccesful member registration", False, "An error occurred while registering the member.", self.userName)

#     def displayMembers(self, db):
#         try:
#             allMembers = db.getMembers()
#             private_key = cryptoUtils.loadPrivateKey()
#             print(f"========List of Members====================================================================================================")
#             if allMembers == None:
#                 print("No members found:")
#             else:
#                 for member in allMembers:
#                     print(f"| Membership ID: {member[0]} | First name: {member[1]} | Last name: {member[2]} | Age: {member[3]} | Gender: {member[4]} | Weight: {member[5]} | Address: {member[6]} | City: {member[7]} | Postal Code: {member[8]} | Email: {member[9]} | Mobile: {member[10]} | Registration Date: {member[11]} |\n")
#             input("Press any key to continue...")
#             return
        
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")

#     def memberSearch(self, db, loggingSys):
#         try:
#             search_key = input("Enter the search key: ")
#             result = db.searchMember(search_key)
            
#             if result:
#                 print("Search Results:")
#                 print("----------------")
#                 for row in result:
#                     print(f"Membership ID: {row[0]}")
#                     print(f"First Name: {row[1]}")
#                     print(f"Last Name: {row[2]}")
#                     print(f"Age: {row[3]}")
#                     print(f"Gender: {row[4]}")
#                     print(f"Weight: {row[5]}")
#                     print(f"Address: {row[6]}")
#                     print(f"City: {row[7]}")
#                     print(f"Postal Code: {row[8]}")
#                     print(f"Email: {row[9]}")
#                     print(f"Mobile: {row[10]}")
#                     print(f"Registration Date: {row[11]}")
#                     print("----------------")
#             else:
#                 print("No results found.")
            
#             input("Press any key to continue...")

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             loggingSys.log(f"Error occurred during member search: {str(e)}", True, username=self.userName)

#     def editMember(self, db, loggingSys):
#         try:
#             self.displayMembers(db)
#             while True:
#                 membershipID = input("Enter the membership ID of the member you would like to edit or press Q to quit: ")
#                 if membershipID.upper() == "Q":
#                     return
#                 if Validation.validateMembershipID(membershipID, self.userName, loggingSys) and db.findMembershipID(membershipID):
#                     break

    def updateTraveller(self, db, loggingSys):
        def safe_decrypt(value):
            try:
                if isinstance(value, bytes):
                    return cryptoUtils.decryptWithPrivateKey(private_key, value).decode()
                return str(value)
            except:
                return "(decryption failed)"
#                 while True:
        # Display all decrypted travellers
        travellers = db.getAllTravellers()
        private_key = cryptoUtils.loadPrivateKey()
#                         return "Q"
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
#                     else:
        license_number = Utility.get_valid_input("Enter the traveller's current driving license number or Q to cancel:", Validation.validate_driving_license, {'username': self.userName}, loggingSys)
        if license_number is None:
            print("Update cancelled.")
            return
#             updates = {}
#             fields_validations = {
#                 "first_name": lambda value: Validation.validateName(value,self.userName,loggingSys),
#                 "last_name": lambda value: Validation.validateName(value,self.userName,loggingSys),
        fields = {}
#                 "weight": lambda value: Validation.validateWeight(value,self.userName,loggingSys),
#                 "address": lambda value: Validation.validateAddress(value,self.userName,loggingSys),
#                 "city": lambda value: Validation.validateCity(value,self.userName,loggingSys),
#                 "postalCode": lambda value: Validation.validateZipcode(value,self.userName,loggingSys),
        new_first = Utility.get_optional_update("New first name:", Validation.validateName, None, {'username': self.userName}, loggingSys)
        if new_first == "Q": return
        if new_first: fields["first_name"] = new_first
#             }
        new_last = Utility.get_optional_update("New last name:", Validation.validateName, None, {'username': self.userName}, loggingSys)
        if new_last == "Q": return
        if new_last: fields["last_name"] = new_last
#                 if input_value == "Q":
#                     print("Edit process terminated by user.")
        new_street = Utility.get_optional_update("New street name:", Validation.validateAddress, None, {'username': self.userName}, loggingSys)
        if new_street == "Q": return
        if new_street: fields["street_name"] = new_street
#                     updates[field] = int(input_value) if field == "age" else float(input_value) if field == "weight" else input_value

#             result = db.updateMember(membershipID, **updates)
#             if result == "OK":
#                 print("Member updated successfully.")
        new_city = Utility.get_optional_update("New city:", Validation.validateCity, None, {'username': self.userName}, loggingSys)
        if new_city == "Q": return
        if new_city: fields["city"] = new_city
#         except Exception as e:
        new_zip = Utility.get_optional_update("New zip code:", Validation.validateZipcode, None, {'username': self.userName}, loggingSys)
        if new_zip == "Q": return
        if new_zip: fields["zip_code"] = new_zip
    def changePassword(self, user, db, loggingSys):
        new_email = Utility.get_optional_update("New email:", Validation.validateEmail, None, {'username': self.userName}, loggingSys)
        if new_email == "Q": return
        if new_email: fields["email"] = new_email
        def processChangePW():
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
                        return
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
            elif isinstance(user, consultant):
                role = roles.CONSULTANT
                processChangePW()
                loggingSys.log(f"Password change", False, username=self.userName)
            else:
                print("Unauthorized access...")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            loggingSys.log(f"Error occurred during password change: {str(e)}", True, username=self.userName)
    
    # def deletion(self, user, db, role, loggingSys):
    #     try:
    #         def processDeletion(role):
    #             roleType = ""
    #             if role == None:
    #                 self.displayMembers(db)
    #                 roleType = "member"
    #             else:
    #                 self.displayUsers(db, role)
    #                 roleType = role.value
    #             validID = False
    #             while True:
    #                 Id = input(f"Enter the ID/membership ID of the {roleType} you would like to delete or enter 'Q' to quit: ").strip()
    #                 if Id.upper() == "Q":
    #                     return
    #                 elif Id.isdigit():
    #                     if not role == None:
    #                         if db.findUserID(int(Id), role):
    #                             validID = True
    #                             break
    #                     else:
    #                         if db.findMembershipID(Id):
    #                            validID = True
    #                            break 
    #                 print("ID not found in the database!" if Id.isdigit() else "ID is invalid!")
    #                 time.sleep(0.5)
    #             if validID:
    #                 if not role == None:
    #                     privateKey = cryptoUtils.loadPrivateKey()
    #                     deletedUsername = db.getUsernameByID(Id)
    #                     result = db.deleteUser(Id, role)
    #                     if result == "OK":
    #                         print("User deleted")
    #                         loggingSys.log("User deleted", False, f"User  '{deletedUsername.decode('utf-8')}' has been deleted.", self.userName)
    #                         deletedUsername = None
    #                     else:
    #                         print("An error occurred while deleting the user.")
    #                         loggingSys.log("Failed to delete user", True, f"An error occurred while deleting the user : {deletedUsername.decode('utf-8')}.", self.userName)
    #                         deletedUsername = None
    #                     time.sleep(1)
    #                 else:
    #                     result = db.deleteMember(Id)
    #                     if result == "OK":
    #                         print("Member deleted")
    #                         loggingSys.log("Member has been deleted", False, username=self.userName)
    #                     else:
    #                         print("An error occurred while deleting the member.")
    #                         loggingSys.log(f"Failed to delete member with id {Id}", True, username=self.userName)
    #                     time.sleep(1)
    #         if role is None:  
    #             if isinstance(user, consultant):
    #                 processDeletion(role)
    #             else:
    #                 print("Unauthorized access...")
    #         elif isinstance(user, superAdministrator):
    #             if role in [None, roles.CONSULTANT, roles.ADMIN]:
    #                 processDeletion(role)
    #             else:
    #                 print("Invalid request....")
    #         elif isinstance(user, systemAdministrator):
    #             if role in [None, roles.CONSULTANT]:
    #                 processDeletion(role)
    #             else:
    #                 print("Unauthorized request.")
    #         else:
    #             print("Unauthorized access...")
    #     except Exception as e:
    #         print(f"An error occurred: {str(e)}")
    #         loggingSys.log(f"Error occurred during deletion: {str(e)}", True, username=self.userName)


class systemAdministrator(consultant):

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

    def createScooter(self, db, loggingSys):
        try:
            print("========== Scooter Registration ==========")
            scooter = {}

            scooter["serial_number"] = Utility.get_valid_input("Enter serial number (SC-XXXXXX):",
                Validation.validateSerialNumber, {"username": self.userName}, loggingSys)

            scooter["brand"] = Utility.get_valid_input("Enter scooter brand:",
                Validation.validateBrandOrModel, {"username": self.userName}, loggingSys)

            scooter["model"] = Utility.get_valid_input("Enter scooter model:",
                Validation.validateBrandOrModel, {"username": self.userName}, loggingSys)

            scooter["top_speed"] = Utility.get_valid_input("Enter top speed (km/h):",
                lambda v, u, l: Validation.validateIntegerInRange(v, 5, 120), {"username": self.userName}, loggingSys)

            scooter["battery_capacity"] = Utility.get_valid_input("Enter battery capacity (Wh):",
                lambda v, u, l: Validation.validateIntegerInRange(v, 100, 2000), {"username": self.userName}, loggingSys)

            scooter["state_of_charge"] = Utility.get_valid_input("Enter current charge (0-100):",
                lambda v, u, l: Validation.validateIntegerInRange(v, 0, 100), {"username": self.userName}, loggingSys)

            scooter["target_soc_min"] = Utility.get_valid_input("Enter minimum charge threshold (0-100):",
                lambda v, u, l: Validation.validateIntegerInRange(v, 0, 100), {"username": self.userName}, loggingSys)

            scooter["target_soc_max"] = Utility.get_valid_input(f'Enter maximum charge threshold ({scooter["target_soc_min"]}-100):',
                lambda v, u, l: Validation.validateIntegerInRange(v, int(scooter["target_soc_min"]), 100), {"username": self.userName}, loggingSys)


            scooter["mileage"] = Utility.get_valid_input("Enter current mileage (default 0):",
                lambda v, u, l: Validation.validateIntegerInRange(v, 0, 999999), {"username": self.userName}, loggingSys)

            # Coordinates
            latitude = input("Enter latitude (e.g. 51.92250): ").strip()
            longitude = input("Enter longitude (e.g. 4.47917): ").strip()

            if not Validation.validateCoordinates(latitude, longitude, {"username": self.userName}, loggingSys):
                print("Invalid GPS coordinates.")
                return
            scooter["latitude"] = latitude
            scooter["longitude"] = longitude

            # Dates
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

    def createBackup(self, user, backUpSystem, loggingSys):
        try:
            while True:
                keyPress = input("Would you like to create a back up [Y/N] ")
                if keyPress.upper() == "Y":
                    print("Creating backup....")
                    backUpSystem.createBackupZip(user)
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
                if role in [roles.ADMIN, roles.SERVICE]:
                    processEdit(role)
                else:
                    print("Invalid request....")
            elif isinstance(user, systemAdministrator):
                if role == roles.SERVICE:
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
                if role in [roles.ADMIN, roles.SERVICE]:
                    processReset(role)
                else:
                    print("Invalid request.")
            elif isinstance(user, systemAdministrator):
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
                if not Validation.validateName(first_name, self.userName, loggingsys):
                    print("Invalid first name. Please try again.")
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