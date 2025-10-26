import re
from datetime import datetime, date

class Validation:

    @staticmethod
    def detectBadInput(input_string):
        return any(ord(c) < 32 or ord(c) == 127 for c in input_string)

    @staticmethod
    def validate(input):
        return bool(re.fullmatch(r"[A-Za-z0-9 !\"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]{1,35}", input))

    @staticmethod
    def validateSerialNumber(serial_number):
        return bool(re.fullmatch(r'^[A-Za-z0-9]{10,17}$', serial_number))

    @staticmethod
    def validateIntegerInRange(value, min_val, max_val):
        return len(value) <= 10 and value.isdigit() and min_val <= int(value) <= max_val

    @staticmethod
    def validateNumericInput(input):
        return bool(re.fullmatch(r'(0|[1-9][0-9]{0,9})', input))
    
    @staticmethod
    def validateBrandOrModel(value):
        return bool(re.fullmatch(r'^[A-Za-z0-9](?:[A-Za-z0-9-]{0,28}[A-Za-z0-9])?$', value))
        
    @staticmethod
    def validateLatitude(latitude):
        return bool(re.fullmatch(r'^\d{2}\.\d{5}$', latitude))
    
    def validateStatus(oos_status):
        return len(oos_status) <= 5 and oos_status.lower() in ["true", "false"]

    @staticmethod
    def validateDate(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            if len(date_str) <= 10:
                return True
        except ValueError:
            return False
        return False
        
    @staticmethod
    def validateLongitude(longitude):
        return bool(re.fullmatch(r'^\d{1,2}\.\d{5}$', longitude))
                                                                        
    @staticmethod
    def validate_birthdate(birthdate):
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", birthdate))

    @staticmethod
    def validate_driving_license(license_number):
        return bool(re.fullmatch(r'^([A-Z]{2}\d{7}|[A-Z]{1}\d{8})$', license_number))

    @staticmethod
    def validateScooterID(scooter_id):
        return len(scooter_id) < 10 and scooter_id.isdigit() and (0 <= int(scooter_id) <= 10000)
    
    @staticmethod
    def usernameValidation(name):
        return bool(re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$", name) or name == "super_admin")
   
    @staticmethod
    def passwordValidation(password):
        if password == "Admin_123?":
            return True
        return bool(re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-])[a-zA-Z0-9~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-]{12,30}$",password))

    @staticmethod
    def validateEmail(email):
        return bool(re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    @staticmethod
    def validateHousenumber(housenumber):
        return  bool(re.fullmatch(r"[1-9]\d{0,3}", housenumber))

    @staticmethod
    def validateZipcode(zip_code):
        return bool(re.fullmatch(r'\d{4}[A-Za-z]{2}', zip_code))

    @staticmethod
    def validateName(name):
        return bool(re.fullmatch(r"[A-Za-z](['-]?[A-Za-z]){0,34}", name))
    
    @staticmethod
    def validateMobileNumber(mobile_number):
        return bool(re.fullmatch(r"\d{8}", mobile_number))
        
    @staticmethod
    def validateMembershipID(membershipID):
        return bool(re.fullmatch(r'[1-9]\d{9}', membershipID))
    
    @staticmethod
    def validateAddress(address):
        return bool(re.fullmatch(r"^[A-Za-z0-9][A-Za-z0-9 '-]{0,34}$", address))

    @staticmethod
    def validateCity(city):
        allowed_cities = {
            'Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 
            'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 
            'Breda', 'Nijmegen'
        }
        return city in allowed_cities
    
    @staticmethod
    def validateBackup(backupName):
        return re.fullmatch(r'^backup([1-9][0-9]*)\.zip$', backupName)
    
    @staticmethod
    def validateGender(gender):
        return gender in ["Male", "Female", "Other"]

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
                
                if result:
                    return True
            else:
                return False

        return False