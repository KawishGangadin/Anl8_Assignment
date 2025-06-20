from pickle import TRUE
import re
from datetime import datetime, date

class Validation:

    @staticmethod
    def validate_length(input, min=1, max=64):
        return min <= len(input) <= max

    @staticmethod
    def validate_num_in_range(input, min, max):
        if Validation.validate_length(input) and Validation.convertableToInt(input):
            return min <= int(input) <= max

    @staticmethod
    def validate_soc(input):
        return Validation.validate_num_in_range(input, 0, 100)

    @staticmethod
    def validate_speed(input):
        return Validation.validate_num_in_range(input, 0, 45)

    @staticmethod
    def validate_batterycap(input):
        return Validation.validate_num_in_range(input, 250, 1000)

    @staticmethod
    def validate_long(input):
        splitInput = input.split(".")
        if len(splitInput) == 2:
            lengthCheck = len(splitInput[1]) == 5
        if Validation.convertableToFloat(input):
            return lengthCheck and 4.41 < float(input) < 4.58 #coordinaat in rotterdam

    @staticmethod
    def validate_lat(input):
        splitInput = input.split(".")
        if len(splitInput) == 2:
            lengthCheck = len(splitInput[1]) == 5
            if Validation.convertableToFloat(input):
                return lengthCheck and 51.86 < float(input) < 51.96 #coordinaat in rotterdam

    @staticmethod
    def validate_oos(input):
        if Validation.validate_length(input):
            try:
                bool(input)
                return True
            except:
                print("Invalid input")
                return False

    @staticmethod
    def validate_mileage(input):
         return Validation.validate_num_in_range(input, 0, 200000)

    @staticmethod
    def validate_serial(input):
        return Validation.validate_length(input, 10, 17) and input.isalnum()

    @staticmethod
    def validate_maintenance_date(input):
        try:
            mdatetime = input.strip()
            mdatetime = datetime.strptime(mdatetime, "%Y-%m-%d").date()
            return Validation.validate_length(input) and mdatetime < date.today() and mdatetime.year > 2010
        except Exception as e:
            print(f"Invalid date: {e}")
        return False

    @staticmethod
    def validate_birthdate(birthdate, username='', loggingSys=None):
        try:
            birthdate = birthdate.strip()
            birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
            if birthdate > date.today():
                return False

            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            return age >= 18

        except ValueError as e:
            if loggingSys:
                loggingSys.log(f"Invalid birthdate format: {e}", False, username=username)
            return False

    @staticmethod
    def validate_driving_license(license_number, username='', loggingSys=None):
        license_number = license_number.strip().upper()
        pattern = r'^([A-Z]{2}\d{7}|[A-Z]{1}\d{8})$'

        if re.fullmatch(pattern, license_number):
            return True

        if loggingSys:
            loggingSys.log("Invalid driving license number format.", False, username=username)
        return False

    @staticmethod
    def checkNullByte(input):
        pattern = r'^[\x20-\x7E]+$' 
        if re.match(pattern, input):
            return True
        return False
    
    @staticmethod
    def usernameValidation(name, username='', loggingSys=None):
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$"
        
        if not isinstance(name, str) or not Validation.checkNullByte(name):
            if loggingSys:
                loggingSys.log(f'Invalid username format or null byte detected in username:', True, username=username)
            return False
        
        try:
            if re.match(pattern, name) or name == "super_admin":
                return True
            else:
                if loggingSys:
                    loggingSys.log(f'Invalid username format (did not match pattern):', False, username=username)
        except re.error:
            if loggingSys:
                loggingSys.log(f'Regex error while validating username:', False, username=username)
        
        return False
        
    @staticmethod
    def passwordValidation(password, username='', loggingSys=None):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+=`|\\(){}[\]:;'<>,.?/-])[a-zA-Z0-9~!@#$%&_+=`|\\(){}[\]:;'<>,.?/-]{12,30}$"
        
        if password == "Admin_123?":
            return True

        if re.match(pattern, password):
            return True
        
        return False
   
    @staticmethod
    def validateEmail(email, username='', loggingSys=None):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not isinstance(email, str) or not Validation.checkNullByte(email):
            if loggingSys:
                loggingSys.log(f'Invalid email format or null byte detected in email:', True, username=username)
            return False
        
        try: 
            if re.match(pattern, email):
                return True
            else: 
                if loggingSys:
                    loggingSys.log(f'Invalid email format (did not match pattern):', False, username=username)
        except re.error:
            if loggingSys:
                loggingSys.log(f'Regex error while validating email:', False, username=username)
        return False 

    @staticmethod
    def validateAge(age, username='', loggingSys=None):
        try:
            age = int(age)
            if 1 <= age <= 100:
                return True
        except ValueError:
            if not isinstance(age, str) or not Validation.checkNullByte(age):
                if loggingSys:
                    loggingSys.log(f'Invalid age format or null byte etected in age:', True, username=username)
            elif loggingSys:
                loggingSys.log(f'Invalid age format (string found) in age:', False, username=username)
            return False
        return False
    
    @staticmethod
    def validateHousenumber(housenumber, username='', loggingSys=None):
        try:
            housenumber = int(housenumber)
            if 1 <= housenumber <= 9999:
                return True
        except ValueError:
            if not isinstance(housenumber, str) or not Validation.checkNullByte(housenumber):
                if loggingSys:
                    loggingSys.log(f'Invalid housenumber format (non-string) or null byte detected in housenumber.', True, username=username)
            elif loggingSys:
                loggingSys.log(f'Invalid housenumber format (string found) in housenumber', False, username=username)
        return False

    @staticmethod
    def validateZipcode(zip_code, username='', loggingSys=None):
        if not isinstance(zip_code, str) or not Validation.checkNullByte(zip_code):
            if loggingSys:
                loggingSys.log(f'Invalid zip code format (non-string) or null byte detected in zip code.', True, username=username)
            return False
        if len(zip_code) == 6 and zip_code[:4].isdigit() and zip_code[4:].isalpha():
            return True
        return False

    @staticmethod
    def validateName(name, username='', loggingSys=None):
        pattern = r"^[A-Za-z]+(['-][A-Za-z]+)*$"
        if re.match(pattern, name) and len(name) <= 35:
            return True
        return False
    
    @staticmethod
    def validateMobileNumber(mobile_number):
        if len(mobile_number) == 8 and mobile_number.isdigit():
            return True
        return False

    @staticmethod
    def convertableToInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def convertableToFloat(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validateID(id, loggingSys=None):
        if Validation.validate_length(id, loggingSys) and Validation.convertableToInt(id):
            id = int(id)
            if 999999999 < id < 10000000000:
                return True
        return False
    
    @staticmethod
    def validateAddress(address, username='', loggingSys=None):
        pattern = r"^[A-Za-z0-9]+([ '-][A-Za-z0-9]+)*$" # regex pattern voor straatnaam: aplhanum characters, spaces, hyphens, and apostrophes

        if not isinstance(address, str) or not Validation.checkNullByte(address):
            if loggingSys:
                loggingSys.log(f"Invalid street name format or null byte detected in address.", True, username=username)
            return False

        if re.match(pattern, address) and len(address) <= 35:
            return True
        else:
            if loggingSys:
                loggingSys.log(f"Invalid street name format (did not match pattern)", False, username=username)
            return False

    @staticmethod
    def validateCity(city, username='', loggingSys=None):
        allowed_cities = {
            'Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 
            'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 
            'Breda', 'Nijmegen'
        }

        if not isinstance(city, str) or not Validation.checkNullByte(city):
            if loggingSys:
                loggingSys.log(f"Invalid city format or null byte detected in city name.", True, username=username)
            return False
        
        if city.strip().title() in allowed_cities:
            return True
        else:
            if loggingSys:
                loggingSys.log(f"Invalid city format (not in allowed cities)", False, username=username)

        return False
    
    @staticmethod
    def validateBackup(backupName, username='', loggingSys=None):
        pattern = r'^backup([1-9][0-9]*)\.zip$'
        if not isinstance(backupName, str) or not Validation.checkNullByte(backupName):
            if loggingSys:
                loggingSys.log(f'Invalid username format or null byte detected in backup input:', True, username=username)
            return False
        
        try:
            if re.match(pattern, backupName):
                return True
            else:
                if loggingSys:
                    loggingSys.log(f'Invalid backup input format (did not match pattern):', False, username=username)
        except re.error:
            if loggingSys:
                loggingSys.log(f'Regex error while validating username:', False, username=username)
        
        return False
    
    @staticmethod
    def validateGender(gender,username='', loggingSys=None):
        if gender.lower() in ["male","female","other"]:
            return True
        if loggingSys:
            loggingSys.log(f'Invalid gender format:', False, username=username)
        return False

    @staticmethod
    def validateWeight(weight,username='', loggingSys=None):
        try:
            weight = float(weight)
            if 10 < weight < 700:
                return True
        except ValueError:
            if loggingSys:
                loggingSys.log(f'Invalid weight format:', False, username=username)
            return False
        if loggingSys:
                loggingSys.log(f'Invalid weight format:', False, username=username)
        return False
    
    @staticmethod
    def validateMultipleInputs(**kwargs):
        validation_mapping = {
            'username': Validation.usernameValidation,
            'password': Validation.passwordValidation,
            'email': Validation.validateEmail,
            'age': Validation.validateAge,
            'housenumber': Validation.validateHousenumber,
            'postalCode': Validation.validateZipcode,
            'first_name': Validation.validateName,
            'last_name': Validation.validateName,
            'mobile': Validation.validateMobileNumber,
            'address': Validation.validateAddress,
            'city': Validation.validateCity,
            'backup': Validation.validateBackup,
            'gender': Validation.validateGender,
        }

        for key, value in kwargs.items():
            if key in validation_mapping:
                validation_func = validation_mapping[key]
                result = validation_func(value)
                
                if not result:
                    return False
            else:
                return False

        return True