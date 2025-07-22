from cryptoUtils import cryptoUtils
from inputValidation import Validation

class Utility:
    @staticmethod
    def get_valid_input(prompt, validator, username="", loggingSys=None, fieldName=None):
        while True:
            value = input(f"{prompt} ")
            if value.upper() == 'Q':
                return None
            elif not Validation.detectBadInput(value):
                if validator(value):
                    return value
                else:
                    print("Invalid input! Please try again.")
                    if loggingSys:
                        loggingSys.log(f"Invalid input ({value}) for field: {fieldName}", False, username)
            else: 
                print("Input contains invalid characters! Please try again.")
                if loggingSys:
                    loggingSys.log(f"Bad input found '({value})' for field: {fieldName}", True, username)


    @staticmethod
    def get_optional_update(prompt, validator, current_value, username="", loggingSys=None, fieldName= None):
        while True:
            value = input(f"{prompt} [Current: {current_value}] (leave empty to keep or Q to quit): ")
            if value.upper() == 'Q':
                return "Q"
            elif value == '':
                return current_value
            elif not Validation.detectBadInput(value):
                if validator(value):
                    return value
                else:
                    print("Invalid input! Please try again.")
                    if loggingSys:
                        loggingSys.log(f"Invalid input ({value}) for field: {fieldName}", False, username)
            else:
                print("Input contains invalid characters! Please try again.")
                if loggingSys:
                    loggingSys.log(f"Bad input found '({value})' for field: {fieldName}", True, username)


    
    @staticmethod
    def safe_decrypt(value):
        private_key = cryptoUtils.loadPrivateKey()
        try:
            if isinstance(value, bytes):
                return cryptoUtils.decryptWithPrivateKey(private_key, value)
            return str(value)
        except:
            print("Decryption failed. Returning original value.")
            

    @staticmethod
    def validateAndParseLongitude():
        pass

    @staticmethod
    def validateAndParseLatitude():
        pass