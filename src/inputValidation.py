import re

class Validation:

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
                loggingSys.log(f'Invalid username format detected in username:', True, username=username)
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
        
        if not isinstance(password, str) or not Validation.checkNullByte(password):
            if loggingSys:
                loggingSys.log(f'Invalid password format null byte, or sql detected in password:', True, username=username)
            return False
        
        try:
            if re.match(pattern, password):
                return True
            else:
                if loggingSys:
                    loggingSys.log(f'Invalid password format (did not match pattern):', False, username=username)
        except re.error:
            if loggingSys:
                loggingSys.log(f'Regex error while validating password:', False, username=username)
        
        return False
   
    @staticmethod
    def validateEmail(email, username='', loggingSys=None):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not isinstance(email, str) or not Validation.checkNullByte(email):
            if loggingSys:
                loggingSys.log(f'Invalid email format null byte, or sql detected in email:', True, username=username)
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
                    loggingSys.log(f'Invalid age format null byte, or sql detected in age:', True, username=username)
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
                    loggingSys.log(f'Invalid housenumber format (non-string), null byte or sql detected in housenumber.', True, username=username)
            elif loggingSys:
                loggingSys.log(f'Invalid housenumber format (string found) in housenumber', False, username=username)
        return False

    @staticmethod
    def validateZipcode(zip_code, username='', loggingSys=None):
        if not isinstance(zip_code, str) or not Validation.checkNullByte(zip_code):
            if loggingSys:
                loggingSys.log(f'Invalid zip code format (non-string), null byte or sql detected in zip code.', True, username=username)
            return False
        if len(zip_code) == 6 and zip_code[:4].isdigit() and zip_code[4:].isalpha():
            return True
        return False

    @staticmethod
    def validateName(name, username='', loggingSys=None):
        pattern = r"^[A-Za-z]+(['-][A-Za-z]+)*$"

        if not isinstance(name, str) or not Validation.checkNullByte(name):
            if loggingSys:
                loggingSys.log(f"Invalid name format (non-string), null-byte or sql detected in name.", True, username=username)
            return False

        if re.match(pattern, name) and len(name) <= 35:
            return True
        else:
            if loggingSys:
                loggingSys.log(f"Invalid name format (did not match pattern).", False, username=username)
            return False
    
    @staticmethod
    def validateMobileNumber(mobile_number, username='', loggingSys=None):
        try: 
            mobile_number = str(mobile_number)
            if len(mobile_number) == 8 and mobile_number.isdigit():
                return True
        except ValueError:
            if not isinstance(mobile_number, str) or not Validation.checkNullByte(mobile_number):
                if loggingSys:
                    loggingSys.log(f"Invalid mobile number format null byte or sql detected in mobile number.", True, username=username)
            else:
                if loggingSys:
                    loggingSys.log(f"Invalid mobile number format (string found) entered.", False, username=username)
        return False

    @staticmethod
    def convertableToInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validateMembershipID(membershipID, username='', loggingSys=None):
        if (Validation.convertableToInt(membershipID)):
            try:
                membershipID = int(membershipID)
                if 999999999 < membershipID < 10000000000:
                    return True
            except ValueError:
                if not isinstance(membershipID, str) or not Validation.checkNullByte(str(membershipID)):
                    if loggingSys:
                        loggingSys.log(f"Invalid membership ID format null byte or sql detected in membership ID", True, username=username)
                    return False
                else:
                    if loggingSys:
                        loggingSys.log(f"Invalid membership ID format (string found)", False, username=username)
                    return False
        else:
            return False
    
    @staticmethod
    def validateAddress(address, username='', loggingSys=None):
        pattern = r"^[A-Za-z0-9]+([ '-][A-Za-z0-9]+)*$" # regex pattern voor straatnaam: aplhanum characters, spaces, hyphens, and apostrophes

        if not isinstance(address, str) or not Validation.checkNullByte(address):
            if loggingSys:
                loggingSys.log(f"Invalid street name format null byte or sql detected in address.", True, username=username)
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
                loggingSys.log(f"Invalid city format null byte or sql detected in city name.", True, username=username)
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
                loggingSys.log(f'Invalid username format null byte or sql detected in backup input:', True, username=username)
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
            'membershipID': Validation.validateMembershipID,
            'address': Validation.validateAddress,
            'city': Validation.validateCity,
            'backup': Validation.validateBackup,
            'gender': Validation.validateGender,
            'weight': Validation.validateWeight
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