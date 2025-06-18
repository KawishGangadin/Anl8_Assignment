from cryptoUtils import cryptoUtils

class Utility:
    @staticmethod
    def get_valid_input(prompt, validator, user=None, loggingSys=None):
        while True:
            value = input(f"{prompt} ").strip()
            if value.upper() == 'Q':
                return None
            if validator(value, user.get('username', '') if user else '', loggingSys):
                return value
            else:
                print("Invalid input! Please try again.")
                if loggingSys and user:
                    loggingSys.log(f"Invalid input for prompt: {prompt}", False, username=user.get('username', ''))

    @staticmethod
    def get_optional_update(prompt, validator, current_value, user=None, loggingSys=None):
        """
        Prompt user for an optional update. If left empty, current_value is returned.
        If 'Q' is entered, returns "Q" to signal cancellation.
        """
        username = user.get('username', '') if user else ''
        while True:
            value = input(f"{prompt} [Current: {current_value}] (leave empty to keep or Q to quit): ").strip()
            if value.upper() == 'Q':
                return "Q"
            if value == '':
                return current_value
            if validator(value, username, loggingSys):
                return value
            else:
                print("Invalid input! Please try again.")
                if loggingSys:
                    loggingSys.log(f"Invalid optional update input for prompt: {prompt}", False, username=username)

    
    @staticmethod
    def safe_decrypt(value):
        private_key = cryptoUtils.loadPrivateKey()
        try:
            if isinstance(value, bytes):
                return cryptoUtils.decryptWithPrivateKey(private_key, value).decode()
            return str(value)
        except:
            return "(decryption failed)"

