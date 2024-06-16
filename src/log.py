import logging
import os
from datetime import datetime
from cryptoUtils import cryptoUtils

class Logger:
    def __init__(self):
        self.log_format = '%(log_number)s | %(asctime)s | %(username)s | %(activity)s | %(additional_info)s | Suspicious: %(suspicious)s | Checked: %(checked)s | %(message)s'
        self.log_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.log_dir, 'logs', 'uniquemeal.log')
        self.checkLogFile()
        self.basicConfig()
        self.public_key = cryptoUtils.loadPublicKey()  # Load the public key correctly
        self.private_key = cryptoUtils.loadPrivateKey()  # Load the private key correctly

    def basicConfig(self):
        logging.basicConfig(filename=self.log_file, filemode='a', level=logging.INFO, format='%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def log(self, activity, suspicious=False, additional_info='-', username='no username'):
        log_number = self.nextNumber()
        log_message = self.log_format % {
            'log_number': log_number,
            'asctime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'activity': activity,
            'additional_info': additional_info,
            'suspicious': suspicious,
            'checked': False,
            'message': ''
        }
        encrypted_message = cryptoUtils.encryptWithPublicKey(self.public_key, log_message)
        logging.info(encrypted_message.hex())

    def checkLogFile(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'):
                pass

    def nextNumber(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                lines = file.readlines()
                return len(lines) + 1
        return 1

    def printLogs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                logs = file.readlines()
                for log in logs:
                    try:
                        decrypted_log = cryptoUtils.decryptWithPrivateKey(self.private_key, bytes.fromhex(log.strip())).decode()
                        print(decrypted_log)
                    except Exception as e:
                        print(f"Error decrypting log: {e}")
            self.markLogs()
        else:
            print("No logs found.")

    def markLogs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                logs = file.readlines()

            with open(self.log_file, 'w') as file:
                for log in logs:
                    try:
                        decrypted_log = cryptoUtils.decryptWithPrivateKey(self.private_key, bytes.fromhex(log.strip())).decode()
                        log_parts = decrypted_log.strip().split('|')
                        if len(log_parts) > 6 and "Checked: False" in log_parts[6]:
                            log_parts[6] = "Checked: True"
                        encrypted_log = cryptoUtils.encryptWithPublicKey(self.public_key, '|'.join(log_parts))
                        file.write(encrypted_log.hex() + "\n")
                    except Exception as e:
                        print(f"Error decrypting log: {e}")
                        file.write(log)  # Write the original log back if decryption fails
            print("All logs have now been marked as checked.")
        else:
            print("No logs found.")
    
    def hasUncheckedSuspiciousLogs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                logs = file.readlines()
                for log in logs:
                    try:
                        decrypted_log = cryptoUtils.decryptWithPrivateKey(self.private_key, bytes.fromhex(log.strip())).decode()
                        log_parts = decrypted_log.strip().split('|')
                        if len(log_parts) > 5 and "Suspicious: True" in log_parts[5] and "Checked: False" in log_parts[6]:
                            return True
                    except Exception as e:
                        print(f"Error decrypting log: {e}")
        return False