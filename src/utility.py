from cryptoUtils import cryptoUtils

class Utility:
    @staticmethod
    def get_valid_input(prompt, validator, username="", loggingSys=None, fieldName=None):
        while True:
            value = input(f"{prompt} ").strip()
            if value.upper() == 'Q':
                return None
            elif validator(value):
                return value
            else:
                print("Invalid input! Please try again.")
                if loggingSys:
                    loggingSys.log(f"Invalid input ({value}) for field: {fieldName}", False, username)


    @staticmethod
    def get_optional_update(prompt, validator, current_value, username="", loggingSys=None, fieldName= None):
        while True:
            value = input(f"{prompt} [Current: {current_value}] (leave empty to keep or Q to quit): ").strip()
            if value.upper() == 'Q':
                return "Q"
            if value == '':
                return current_value
            if validator(value):
                return value
            else:
                print("Invalid input! Please try again.")
                if loggingSys:
                    loggingSys.log(f"Invalid input ({value}) for field: {fieldName}", False, username)


    
    @staticmethod
    def safe_decrypt(value):
        private_key = cryptoUtils.loadPrivateKey()
        try:
            if isinstance(value, bytes):
                return cryptoUtils.decryptWithPrivateKey(private_key, value)
            return str(value)
        except:
            print("Decryption failed. Returning original value.")
            

