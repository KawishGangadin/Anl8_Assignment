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
