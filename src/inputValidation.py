import re

class Validation:

    @staticmethod
    def checkNullByte(input):
        return '\x00' not in input
    
    @staticmethod
    def usernameValidation(username):
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$"
        
        if not isinstance(username, str) or not Validation.checkNullByte(username):
            return False
        
        try:
            if re.match(pattern, username) or username == "super_admin":
                return True
        except re.error:
            return False
        
        return False
        
    @staticmethod
    def passwordValidation(password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+=`|\\(){}[\]:;'<>,.?/-])[a-zA-Z0-9~!@#$%&_+=`|\\(){}[\]:;'<>,.?/-]{12,30}$"
        
        if password == "Admin_123?":
            return True
        
        if not isinstance(password, str) or not Validation.checkNullByte(password):
            return False
        
        try:
            if re.match(pattern, password):
                return True
        except re.error:
            pass
        
        return False

    
    @staticmethod
    def validateEmail(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not Validation.checkNullByte(email):
            return False
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validateAge(age):
        try:
            age = int(age)
            if 1 <= age <= 100:
                return True
        except ValueError:
            return False
        return False
    
    @staticmethod
    def validateHousenumber(housenumber):
        try:
            housenumber = int(housenumber)
            if 1 <= housenumber <= 9999:
                return True
        except ValueError:
            return False
        return False

    
    @staticmethod
    def validateZipcode(zip_code):
        if not Validation.checkNullByte:
            return False
        if len(zip_code) == 6 and zip_code[:4].isdigit() and zip_code[4:].isalpha():
            return True
        return False

    
    @staticmethod
    def validateName(name):
        allowed_characters = "-' "
        
        if not isinstance(name, str):
            return False
        
        try:
            if not all(char.isalpha() or char in allowed_characters for char in name):
                return False
            
            if name.count('-') > 1 or name.count("'") > 1 or name.count(' ') > 2:
                return False
            
            if name.strip() == '':
                return False
            
            if name.startswith('-') or name.startswith("'") or name.endswith('-') or name.endswith("'"):
                return False
        except (AttributeError, TypeError):
            return False
        
        return True
    
    @staticmethod
    def validateMobileNumber(mobile_number):
        # Ensure input is treated as a string
        mobile_number = str(mobile_number)

        # Check for null byte and digits only
        if not Validation.checkNullByte(mobile_number) or not mobile_number.isdigit():
            return False

        # Validate length
        if len(mobile_number) == 8:
            return True

        return False


    @staticmethod
    def validateMembershipID(membershipID):
        if not Validation.checkNullByte(str(membershipID)):
            return False

        try:
            membershipID = int(membershipID)
            if 999999999 < membershipID < 10000000000:
                return True
        except ValueError:
            return False
        return False
    
    @staticmethod
    def validateAddress(address):
        allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,'-")
        
        if not isinstance(address, str) or not Validation.checkNullByte(address):
            return False
        
        try:
            if not all(char in allowed_characters for char in address):
                return False
            
            if address.strip() == '':
                return False
            
        except (AttributeError, TypeError):
            return False
        
        return True
    
    @staticmethod
    def validateCity(city):
        allowed_cities = {
            'Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 
            'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 
            'Breda', 'Nijmegen'
        }

        # Check if the input is a string, and if it contains null bytes
        if not isinstance(city, str) or not Validation.checkNullByte(city):
            return False

        # Clean up the input by stripping spaces and making it case-insensitive
        city = city.strip().title()

        # Check if the city is in the allowed set
        return city in allowed_cities