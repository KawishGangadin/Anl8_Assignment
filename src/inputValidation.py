import re
from datetime import datetime, date

class InputValidation:

    @staticmethod
    def Validate(input):
        return bool(re.fullmatch(r"[A-Za-z0-9 !\"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]{1,35}", input))

    @staticmethod
    def ValidateSerialNumber(serial_number):
        return bool(re.fullmatch(r'^[A-Za-z0-9]{10,17}$', serial_number))

    @staticmethod
    def ValidateNumericInput(input):
        return bool(re.fullmatch(r'(0|[1-9][0-9]{0,9})', input))
    
    @staticmethod
    def ValidateBrandOrModel(value):
        return bool(re.fullmatch(r'^[A-Za-z0-9](?:[A-Za-z0-9-]{0,28}[A-Za-z0-9])?$', value))
    
    def ValidateStatus(oos_status):
        return oos_status in ["true", "false"]

    def ValidateDecimal(value):
        return bool(re.fullmatch(r'^\d{1,2}\.\d{5}$', value))

    @staticmethod
    def ValidateDateFormat(birthdate):
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", birthdate))
    
    @staticmethod
    def ValidateSpeed(speed) -> bool:
        return re.fullmatch(r"([1-9]|[1-4][0-9]|5[0])", speed) is not None
    
    @staticmethod
    def ValidateUsername(name):
        return bool(re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$", name))
   
    @staticmethod
    def ValidatePassword(password):
        return bool(re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-])[a-zA-Z0-9~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-]{12,30}$",password))

    @staticmethod
    def ValidateEmailAddress(email):
        return bool(re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    @staticmethod
    def ValidateHousenumber(houseNumber):
        return bool(re.fullmatch(r"[1-9]\d{0,5}[A-Za-z]?", houseNumber))

    @staticmethod 
    def ValidateDrivingLicense(license_number): 
        return bool(re.fullmatch(r'^([A-Z]{2}\d{7}|[A-Z]{1}\d{8})$', license_number))

    @staticmethod
    def ValidateZipcode(zip_code):
        return bool(re.fullmatch(r'\d{4}[A-Za-z]{2}', zip_code))

    @staticmethod
    def ValidateName(name):
        return re.fullmatch(r"[A-Za-z](['-]?[A-Za-z]){0,34}", name) is not None
    
    @staticmethod
    def ValidateMobileNumber(mobile_number):
        return re.fullmatch(r"\d{8}", mobile_number) is not None
        
    @staticmethod
    def ValidateMembershipID(membershipID):
        return re.fullmatch(r'[1-9]\d{9}', membershipID) is not None
    
    @staticmethod
    def ValidateAddress(address):
        return re.fullmatch(r"^[A-Za-z][A-Za-z '-]{0,34}$", address) is not None

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
        return re.fullmatch(r'^backup([1-9][0-9]*)\.zip$', backupName) is not None
    
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