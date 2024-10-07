import re

class Validation:

    @staticmethod
    def checkNullByte(input):
        if '\x00' in input:
            return False
        return True
    
    @staticmethod
    def checkSqlInjection(input):
        sql_injection_keywords = [";", "--", "/*", "*/", "xp_", "UNION", "SELECT", "INSERT", "DELETE", "DROP"]
        if any(keyword in input.upper() for keyword in sql_injection_keywords):
            return False
        return True
    
    @staticmethod
    def usernameValidation(name, username='', loggingSys=None):
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$"
        
        if not isinstance(name, str) or not Validation.checkNullByte(name) or not Validation.checkSqlInjection(name):
            if loggingSys:
                loggingSys.log(f'Invalid username format (non-string) null byte, or sql detected in username: {name}', True, username=username)
            return False
        
        try:
            if re.match(pattern, name) or name == "super_admin":
                return True
            else:
                if loggingSys:
                    loggingSys.log(f'Invalid username format (did not match pattern): {name}', False, username=username)
        except re.error:
            if loggingSys:
                loggingSys.log(f'Regex error while validating username: {name}', False, username=username)
        
        return False
        
    @staticmethod
    def passwordValidation(password, username='', loggingSys=None):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+=`|\\(){}[\]:;'<>,.?/-])[a-zA-Z0-9~!@#$%&_+=`|\\(){}[\]:;'<>,.?/-]{12,30}$"
        
        if password == "Admin_123?":
            return True
        
        if not isinstance(password, str) or not Validation.checkNullByte(password) or not Validation.checkSqlInjection(password):
            if loggingSys:
                loggingSys.log(f'Invalid password format (non-string) or null byte, or sql detected in password: {password}', True, username=username)
            return False
        
        try:
            if re.match(pattern, password):
                return True
            else:
                if loggingSys:
                    loggingSys.log(f'Invalid password format (did not match pattern): {password}', False, username=username)
        except re.error:
            if loggingSys:
                loggingSys.log(f'Regex error while validating password: {password}', False, username=username)
        
        return False

    
    @staticmethod
    def validateEmail(email, username='', loggingSys=None):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not isinstance(email, str) or not Validation.checkNullByte(email) or not Validation.checkSqlInjection(email):
            if loggingSys:
                loggingSys.log(f'Invalid email format (non-string) or null byte, or sql detected in email: {email}', True, username=username)
            return False
        
        try: 
            if re.match(pattern, email):
                return True
            else: 
                if loggingSys:
                    loggingSys.log(f'Invalid email format (did not match pattern): {email}', False, username=username)
        except re.error:
            if loggingSys:
                loggingSys.log(f'Regex error while validating email: {email}', False, username=username)
        return False 
    
    @staticmethod
    def validateAge(age, username='', loggingSys=None):
        try:
            age = int(age)
            if 1 <= age <= 100:
                return True
        except ValueError:
            if not isinstance(age, str) or not Validation.checkNullByte(age) or not Validation.checkSqlInjection(age):
                if loggingSys:
                    loggingSys.log(f'Invalid age format (non-string) or null byte, or sql detected in age: {age}', True, username=username)
            elif loggingSys:
                loggingSys.log(f'Invalid age format (string found) in age: {age}', False, username=username)
            return False
        return False
    
    @staticmethod
    def validateHousenumber(housenumber, username='', loggingSys=None):
        try:
            housenumber = int(housenumber)
            if 1 <= housenumber <= 9999:
                return True
        except ValueError:
            if not isinstance(housenumber, str) or not Validation.checkNullByte(housenumber) or not Validation.checkSqlInjection(housenumber):
                if loggingSys:
                    loggingSys.log(f'Invalid housenumber format (non-string), null byte or sql detected in housenumber: {housenumber}', True, username=username)
            elif loggingSys:
                loggingSys.log(f'Invalid housenumber format (string found) in housenumber: {housenumber}', False, username=username)
        return False

    
    @staticmethod
    def validateZipcode(zip_code, username='', loggingSys=None):
        if not isinstance(zip_code, str) or not Validation.checkNullByte(zip_code) or not Validation.checkSqlInjection(zip_code):
            if loggingSys:
                loggingSys.log(f'Invalid zip code format (non-string), null byte or sql detected in zip code: {zip_code}', True, username=username)
            return False
        if len(zip_code) == 6 and zip_code[:4].isdigit() and zip_code[4:].isalpha():
            return True
        return False

    
    @staticmethod
    def validateName(name, username='', loggingSys=None):
        pattern = r"^[A-Za-z]+([ '-][A-Za-z]+)*$"

        if not isinstance(name, str) or not Validation.checkNullByte(name) or not Validation.checkSqlInjection(name):
            loggingSys.log(f"Invalid name format (non-string), null-byte or sql detected in name: {name}.", True, username=username)
            return False

        if re.match(pattern, name):
            return True
        else:
            loggingSys.log(f"Invalid name format (did not match pattern): {name}", False, username=username)
            return False
    
    @staticmethod
    def validateMobileNumber(mobile_number, username='', loggingSys=None):
        try: 
            mobile_number = str(mobile_number)
            if len(mobile_number) == 8 and mobile_number.isdigit():
                return True
        except ValueError:
            if not isinstance(mobile_number, str) or not Validation.checkNullByte(mobile_number) or not Validation.checkSqlInjection(mobile_number):
                loggingSys.log(f"Invalid mobile number format (non-string), null byte or sql detected in mobile number: {mobile_number}.", True, username=username)
            else:
                loggingSys.log(f"Invalid mobile number format (string found) entered by {username}.", False, username=username)
        return False


    @staticmethod
    def validateMembershipID(membershipID, username='', loggingSys=None):
        try:
            membershipID = int(membershipID)
            if 999999999 < membershipID < 10000000000:
                return True
        except ValueError:
            if not isinstance(membershipID, str) or not Validation.checkNullByte(str(membershipID)) or not Validation.checkSqlInjection(str(membershipID)):
                loggingSys.log(f"Invalid membership ID format (non-string), null byte or sql detected in membership ID: {membershipID}", True, username=username)
            else:
                loggingSys.log(f"Invalid membership ID format (string found): {membershipID}", False, username=username)
        return False
    
    @staticmethod
    def validateAddress(address, username='', loggingSys=None):
        pattern = r"^[A-Za-z0-9]+([ '-][A-Za-z0-9]+)*$" # regex pattern voor straatnaam: aplhanum characters, spaces, hyphens, and apostrophes

        if not isinstance(address, str) or not Validation.checkNullByte(address) or not Validation.checkSqlInjection(address):
            loggingSys.log(f"Invalid street name format (non-string), null byte or sql detected in address: {address}.", True, username=username)
            return False

        if re.match(pattern, address):
            return True
        else:
            loggingSys.log(f"Invalid street name format (did not match pattern): {address}", False, username=username)
            return False

    @staticmethod
    def validateCity(city, username='', loggingSys=None):
        allowed_cities = {
            'Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 
            'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 
            'Breda', 'Nijmegen'
        }

        if not isinstance(city, str) or not Validation.checkNullByte(city) or not Validation.checkSqlInjection(city):
            loggingSys.log(f"Invalid city format (non-string), null byte or sql detected in city name: {city}.", True, username=username)
            return False
        
        if city.strip().title() in allowed_cities:
            return True
        else:
            loggingSys.log(f"Invalid city format (not in allowed cities): {city}", False, username=username)

        return False