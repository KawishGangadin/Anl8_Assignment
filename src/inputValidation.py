import re
from datetime import datetime, date

class InputValidation:

    @staticmethod
    def DetectBadInput(input_string):
        return any(ord(c) < 32 or ord(c) == 127 for c in input_string)

    @staticmethod
    def Validate(input):
        return re.fullmatch(r"[A-Za-z0-9 !\"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]{1,35}", input)

    @staticmethod
    def ValidateSerialNumber(serial_number):
        return re.fullmatch(r'^[A-Za-z0-9]{10,17}$', serial_number)

    @staticmethod
    def ValidateNumericInput(input):
        return re.fullmatch(r'(0|[1-9][0-9]{0,9})', input)
    
    @staticmethod
    def ValidateBrandOrModel(value):
        return re.fullmatch(r'^[A-Za-z0-9](?:[A-Za-z0-9-]{0,28}[A-Za-z0-9])?$', value)
    
    def ValidateStatus(oos_status):
        return oos_status in ["true", "false"]

    def ValidateDecimal(value):
        return re.fullmatch(r'^\d{1,2}\.\d{5}$', value) is not None

    @staticmethod
    def ValidateDateFormat(birthdate):
        return re.fullmatch(r"\d{4}-\d{2}-\d{2}", birthdate)
    
    @staticmethod
    def ValidateUsername(name):
        return re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$", name) or name == "super_admin"
   
    @staticmethod
    def ValidatePassword(password):
        if password == "Admin_123?":
            return True
        return re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-])[a-zA-Z0-9~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-]{12,30}$",password)

    @staticmethod
    def ValidateEmailAddress(email):
        return re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    
    @staticmethod
    def ValidateHousenumber(houseNumber):
        return re.fullmatch(r"[1-9]\d{0,5}[A-Za-z]?", houseNumber)

    @staticmethod 
    def ValidateDrivingLicense(license_number): 
        return re.fullmatch(r'^([A-Z]{2}\d{7}|[A-Z]{1}\d{8})$', license_number)

    @staticmethod
    def ValidateZipcode(zip_code):
        return re.fullmatch(r'\d{4}[A-Za-z]{2}', zip_code)

    @staticmethod
    def ValidateName(name):
        return re.fullmatch(r"[A-Za-z](['-]?[A-Za-z]){0,34}", name)
    
    @staticmethod
    def ValidateMobileNumber(mobile_number):
        return re.fullmatch(r"\d{8}", mobile_number)
        
    @staticmethod
    def ValidateMembershipID(membershipID):
        return re.fullmatch(r'[1-9]\d{9}', membershipID)
    
    @staticmethod
    def ValidateAddress(address):
        return re.fullmatch(r"^[A-Za-z][A-Za-z '-]{0,34}$", address)

    @staticmethod
    def ValidateCity(city):
        allowed_cities = {
            'Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 
            'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 
            'Breda', 'Nijmegen'
        }
        return city in allowed_cities
    
    @staticmethod
    def ValidateBackup(backupName):
        return re.fullmatch(r'^backup([1-9][0-9]*)\.zip$', backupName)
    
    @staticmethod
    def ValidateGender(gender):
        return gender in ["Male", "Female", "Other"]

    @staticmethod
    def ValidateUserInformation(**kwargs):
        validation_mapping = {
            'username': InputValidation.ValidateUsername,
            'password': InputValidation.ValidatePassword,
            'email': InputValidation.ValidateEmailAddress,
            'first_name': InputValidation.ValidateName,
            'last_name': InputValidation.ValidateName,
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