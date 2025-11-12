from datetime import datetime
from cryptoUtils import CryptoUtils
from inputValidation import InputValidation
import base64
import secrets
import sys

class Utility:
    @staticmethod
    def GetValidInput(prompt, validator, username="", loggingSys=None, fieldName=None):
        while True:
            value = input(f"{prompt} ")
            if value.upper() == 'Q':
                return None
            if not InputValidation.DetectBadInput(value):
                if bool(validator(value)):
                    return value
                else:
                    print("Invalid input! Please try again.")
                    if loggingSys:
                        loggingSys.Log(f"Invalid input ({value}) for field: {fieldName}", False, username)
            else:
                print("Input contains invalid characters! Please try again.")
                if loggingSys:
                    loggingSys.Log(f"Bad input found '({value})' for field: {fieldName}", True, username)

    @staticmethod
    def GetOptionalUpdate(prompt, validator, current_value, username="", loggingSys=None, fieldName=None):
        while True:
            value = input(f"{prompt} [Current: {current_value}] (leave empty to keep or Q to quit): ")
            if value.upper() == 'Q':
                return "Q"
            if value == '':
                return current_value
            if not InputValidation.DetectBadInput(value):
                if bool(validator(value)):
                    return value
                else:
                    print("Invalid input! Please try again.")
                    if loggingSys:
                        loggingSys.Log(f"Invalid input ({value}) for field: {fieldName}", False, username)
            else:
                print("Input contains invalid characters! Please try again.")
                if loggingSys:
                    loggingSys.Log(f"Bad input found '({value})' for field: {fieldName}", True, username)


    
    @staticmethod
    def SafeDecrypt(value):
        private_key = CryptoUtils.LoadPrivateKey()
        try:
            if isinstance(value, bytes):
                return CryptoUtils.DecryptWithPrivateKey(private_key, value)
            return str(value)
        except:
            print("Decryption failed.")
            return None
            
    @staticmethod
    def GenerateSessionID(length: int = 32):
        """
        Generates a secure, URL-safe session ID.
        - `length` is the number of bytes before encoding (default 32 = 256-bit key).
        """
        random_bytes = secrets.token_bytes(length)
        session_id = base64.urlsafe_b64encode(random_bytes).rstrip(b'=').decode('utf-8')
        return session_id

    @staticmethod
    def ValidateLatitude(latitudeValue):
        rotterdamMinLat = 51.80
        rotterdamMaxLat = 52.05

        if not InputValidation.ValidateDecimal(latitudeValue):
            return False

        try:
            latitudeNumber = float(latitudeValue)
        except ValueError:
            return False

        return rotterdamMinLat <= latitudeNumber <= rotterdamMaxLat

    @staticmethod
    def ValidateLongtitude(longitudeValue):
        rotterdamMinLon = 3.90
        rotterdamMaxLon = 4.80
        if not InputValidation.ValidateDecimal(longitudeValue):
            return False

        try:
            longitudeNumber = float(longitudeValue)
        except ValueError:
            return False

        return rotterdamMinLon <= longitudeNumber <= rotterdamMaxLon

    @staticmethod
    def ValidateIntegerInRange(value, minVal, maxVal):

        if not (
            InputValidation.ValidateNumericInput(value)
            and InputValidation.ValidateNumericInput(minVal)
            and InputValidation.ValidateNumericInput(maxVal)
        ):
            return False

        number   = int(value)
        minValue = int(minVal)
        maxValue = int(maxVal)

        if minValue > maxValue:
            return False

        return minValue <= number <= maxValue


    @staticmethod
    def ValidateDate(date):
        if not InputValidation.ValidateDateFormat(date):
            return False
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
