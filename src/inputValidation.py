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
        return isinstance(value, str) and len(value) <= 10 and value.isdigit() and min_val <= int(value) <= max_val

    @staticmethod
    def validateNumericInput(input):
        return bool(re.fullmatch(r'(0|[1-9][0-9]{0,9})', input))
    
    @staticmethod
    def validateBrandOrModel(value):
        return bool(re.fullmatch(r'^[A-Za-z0-9](?:[A-Za-z0-9-]{0,28}[A-Za-z0-9])?$', value))
        
    @staticmethod
    def validateLatitude(latitude):
        if not isinstance(latitude, str):
            return False
        if not re.fullmatch(r'^\d{2}\.\d{5}$', latitude):
            return False
        lat = float(latitude)
        return 51.85 <= lat <= 52.05
    
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
        if isinstance(longitude, str) and re.fullmatch(r'^\d{1,2}\.\d{5}$', longitude) and 4.35 <= float(longitude) <= 4.55:
            return True

    @staticmethod
    def validate_birthdate(birthdate):
        try:
            birthdate_str = birthdate
            birthdate = birthdate.strip()
            birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()

            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            return len(birthdate_str) <= 12 and birthdate < date.today() and age >= 18

        except ValueError as e:
            return False

    @staticmethod
    def validate_driving_license(license_number):
        return isinstance(license_number, str) and bool(re.fullmatch(r'^([A-Z]{2}\d{7}|[A-Z]{1}\d{8})$', license_number.strip().upper()))

    @staticmethod
    def validateScooterID(scooter_id):
        return isinstance(scooter_id, str) and len(scooter_id) < 10 and scooter_id.isdigit() and (0 <= int(scooter_id) <= 10000)
    
    @staticmethod
    def usernameValidation(name):
        return isinstance(name, str) and (bool(re.fullmatch(r"^[a-zA-Z_][a-zA-Z0-9_.']{7,9}$", name)) or name == "super_admin")
   
    @staticmethod
    def passwordValidation(password):
        if password == "Admin_123?":
            return True
        return isinstance(password, str) and bool(re.fullmatch(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-])[a-zA-Z0-9~!@#$%&_+=`|\\(){}\[\]:;'<>,.?/-]{12,30}$",
            password))

    @staticmethod
    def validateEmail(email):
        return isinstance(email, str) and bool(re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    @staticmethod
    def validateHousenumber(housenumber):
        return isinstance(housenumber, str) and len(housenumber) <= 10 and housenumber.isdigit() and 1 <= int(housenumber) <= 9999

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
        return isinstance(membershipID, str) and len(membershipID) <= 10 and membershipID.isdigit() and 999999999 < int(membershipID) < 10000000000
    
    @staticmethod
    def validateAddress(address):
        return isinstance(address, str) and bool(re.fullmatch(r"^[A-Za-z0-9]+([ '-][A-Za-z0-9]+)*$", address)) and len(address) <= 35

    @staticmethod
    def validateCity(city):
        allowed_cities = {
            'amsterdam', 'rotterdam', 'the hague', 'utrecht', 
            'eindhoven', 'tilburg', 'groningen', 'almere', 
            'breda', 'nijmegen'
        }
        return isinstance(city, str) and city.lower() in allowed_cities
    
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
                
                if result:
                    return True
            else:
                return False

        return False
    

print(Validation.validateNumericInput("asdasd6-asd"))
print(Validation.validateNumericInput("6\x006"))
print(Validation.validateNumericInput("66"))
print(Validation.validateNumericInput("0066"))