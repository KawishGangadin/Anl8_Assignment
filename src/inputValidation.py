import re
from datetime import datetime, date

class Validation:

    @staticmethod
    def detectBadInput(input_string):
        return any(ord(c) < 32 or ord(c) == 127 for c in input_string)

    @staticmethod
    def validateSerialNumber(serial_number):
        return isinstance(serial_number, str) and bool(re.fullmatch(r'^[A-Za-z0-9]{10,17}$', serial_number.strip()))

    @staticmethod
    def validateIntegerInRange(value, min_val, max_val):
        return isinstance(value, str) and value.isdigit() and min_val <= int(value) <= max_val

    @staticmethod
    def validateBrandOrModel(value):
        return isinstance(value, str) and bool(re.fullmatch(r'^[A-Za-z0-9-]{2,30}$', value))
        
    @staticmethod
    def validateLatitude(latitude):
        if not isinstance(latitude, str):
            return False
        if not re.fullmatch(r'^\d{2}\.\d{5}$', latitude):
            return False
        lat = float(latitude)
        return 51.85 <= lat <= 52.05

    @staticmethod
    def validateDate(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validateLongitude(longitude):
        if not isinstance(longitude, str):
            return False
        if not re.fullmatch(r'^\d{1,2}\.\d{5}$', longitude):
            return False
        lon = float(longitude)
        return 4.35 <= lon <= 4.55

    @staticmethod
    def validate_birthdate(birthdate):
        try:
            birthdate = birthdate.strip()
            birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
            if birthdate > date.today():
                return False

            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            return age >= 18

        except ValueError as e:
            return False

    @staticmethod
    def validate_driving_license(license_number):
        return isinstance(license_number, str) and bool(re.fullmatch(r'^([A-Z]{2}\d{7}|[A-Z]{1}\d{8})$', license_number.strip().upper()))

    
    @staticmethod
    def usernameValidation(name):
        return isinstance(name, str) and (bool(re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$", name)) or name == "super_admin")
   
    @staticmethod
    def passwordValidation(password):
        if password == "Admin_123?":
            return True
        if not isinstance(password, str):
            return False
        return bool(re.fullmatch(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-])[a-zA-Z0-9~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-]{12,30}$",
            password))

    @staticmethod
    def validateEmail(email):
        return isinstance(email, str) and bool(re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    @staticmethod
    def validateHousenumber(housenumber):
        return isinstance(housenumber, str) and housenumber.isdigit() and 1 <= int(housenumber) <= 9999

    @staticmethod
    def validateZipcode(zip_code):
        return isinstance(zip_code, str) and len(zip_code) == 6 and zip_code[:4].isdigit() and zip_code[4:].isalpha()

    @staticmethod
    def validateName(name):
        return isinstance(name, str) and bool(re.fullmatch(r"^[A-Za-z]+(['-][A-Za-z]+)*$", name)) and len(name) <= 35
    
    @staticmethod
    def validateMobileNumber(mobile_number):
        return isinstance(mobile_number, str) and mobile_number.isdigit() and len(mobile_number) == 8
        
    @staticmethod
    def validateMembershipID(membershipID):
        return isinstance(membershipID, str) and membershipID.isdigit() and 999999999 < int(membershipID) < 10000000000
    
    @staticmethod
    def validateAddress(address):
        return isinstance(address, str) and bool(re.fullmatch(r"^[A-Za-z0-9]+([ '-][A-Za-z0-9]+)*$", address)) and len(address) <= 35

    @staticmethod
    def validateCity(city):
        allowed_cities = {
            'Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 
            'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 
            'Breda', 'Nijmegen'
        }
        return isinstance(city, str) and city in allowed_cities
    
    @staticmethod
    def validateBackup(backupName):
        return isinstance(backupName, str) and bool(re.fullmatch(r'^backup([1-9][0-9]*)\.zip$', backupName))
    
    @staticmethod
    def validateGender(gender):
        return isinstance(gender, str) and gender.lower() in ["male", "female", "other"]

    @staticmethod
    def validateMultipleInputs(**kwargs):
        validation_mapping = {
            'username': Validation.usernameValidation,
            'password': Validation.passwordValidation,
            'email': Validation.validateEmail,
            'first_name': Validation.validateName,
            'last_name': Validation.validateName,
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