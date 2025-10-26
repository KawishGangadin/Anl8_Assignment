from datetime import datetime
from cryptoUtils import cryptoUtils
from inputValidation import Validation
import base64
import secrets
import sys

class Utility:
    @staticmethod
    def get_valid_input(prompt, validator, username="", loggingSys=None, fieldName=None):
        while True:
            value = input(f"{prompt} ")
            if value.upper() == 'Q':
                return None
            if not Validation.detectBadInput(value):
                if bool(validator(value)):
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
    def get_optional_update(prompt, validator, current_value, username="", loggingSys=None, fieldName=None):
        while True:
            value = input(f"{prompt} [Current: {current_value}] (leave empty to keep or Q to quit): ")
            if value.upper() == 'Q':
                return "Q"
            if value == '':
                return current_value
            if not Validation.detectBadInput(value):
                if bool(validator(value)):
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
            print("Decryption failed.")
            return None
            
    @staticmethod
    def generate_session_id(length: int = 32):
        """
        Generates a secure, URL-safe session ID.
        - `length` is the number of bytes before encoding (default 32 = 256-bit key).
        """
        random_bytes = secrets.token_bytes(length)
        session_id = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode('utf-8')
        return session_id

    @staticmethod
    def ValidateLongtitude():
        pass

    @staticmethod
    def ValidateLatitude():
        pass

    @staticmethod
    def ValidateBirthdate(Birthdate: str) -> bool:
        if not Validation.ValidateDateFormat(Birthdate):
            return False
        try:
            datetime.strptime(Birthdate, "%Y-%m-%d")
            return True
        except ValueError:
            return False
