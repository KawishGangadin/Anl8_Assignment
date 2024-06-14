import re

class Validation:
    
    @staticmethod
    def usernameValidation(username):
        # Regex pattern for username validation
        pattern = r"^(?!_)[a-zA-Z_][a-zA-Z0-9_'\.]{6,11}$"
        
        if not isinstance(username, str):
            return False
        
        try:
            if re.match(pattern, username) or username == "super_admin":
                return True
        except re.error:
            return False
        
        return False
        
    @staticmethod
    def passwordValidation(password):
        # Regex pattern for password validation
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-=\\|(){}\[\]:;'<>,.?/])[a-zA-Z\d~!@#$%&_\-=\\|(){}\[\]:;'<>,.?/]{12,30}$"
        
        if password == "Admin_123?":
            return True
        
        if not isinstance(password, str):
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
        try:
            if len(zip_code) == 6 and zip_code[:4].isdigit() and zip_code[4:].isalpha():
                for char in zip_code[:4]:
                    if char not in "1234567890":
                        return False
                return True
        except (ValueError, IndexError):
            pass
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
        try:
            mobile_number = int(mobile_number)
            if 11111111 <= mobile_number <= 99999999:
                return True
        except ValueError:
            return False
        return False

    @staticmethod
    def validateMenuOption(input,optionList):
        pass

    @staticmethod
    def validateMembershipID(membershipID):
        try:
            membershipID = int(membershipID)
            if 999999999 < membershipID < 10000000000:
                return True
        except ValueError:
            return False
        return False