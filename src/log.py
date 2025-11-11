import logging
import os
from datetime import datetime
from cryptoUtils import CryptoUtils

class Logger:
    def __init__(self):
        self.log_format = '%(log_number)s | %(asctime)s | %(username)s | %(activity)s | %(additional_info)s | Suspicious: %(suspicious)s | Checked: %(checked)s | %(message)s'
        self.log_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.log_dir, 'logs', 'urbanmobility.log')
        self.CheckLogFile()
        self.BasicConfig()
        self.public_key = CryptoUtils.LoadPublicKey() 
        self.private_key = CryptoUtils.LoadPrivateKey() 

    def BasicConfig(self):
        logging.basicConfig(filename=self.log_file, filemode='a', level=logging.INFO, format='%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def Log(self, activity, suspicious=False, additional_info='-', username='no username'):
        logNumber = self.NextNumber()
        logMessage = self.log_format % {
            'log_number': logNumber,
            'asctime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'activity': activity,
            'additional_info': additional_info,
            'suspicious': suspicious,
            'checked': False,
            'message': ''
        }
        encrypted_message = CryptoUtils.EncryptWithPublicKey(self.public_key, logMessage)
        logging.info(encrypted_message.hex())

    def CheckLogFile(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'):
                pass

    def NextNumber(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                lines = file.readlines()
                return len(lines) + 1
        return 1

    def PrintLogs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                logs = file.readlines()
                for log in logs:
                    try:
                        decrypted_log = CryptoUtils.DecryptWithPrivateKey(self.private_key, bytes.fromhex(log.strip()))
                        print("-"* len(decrypted_log))
                        print(decrypted_log)
                    except Exception as e:
                        print(f"Error decrypting log: {e}")
            self.MarkLogs()
        else:
            print("No logs found.")

    def MarkLogs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                logs = file.readlines()

            with open(self.log_file, 'w') as file:
                for log in logs:
                    try:
                        decrypted_log = CryptoUtils.DecryptWithPrivateKey(self.private_key, bytes.fromhex(log.strip()))
                        log_parts = decrypted_log.strip().split('|')
                        if len(log_parts) > 6 and "Checked: False" in log_parts[6]:
                            log_parts[6] = "Checked: True"
                        encrypted_log = CryptoUtils.EncryptWithPublicKey(self.public_key, '|'.join(log_parts))
                        file.write(encrypted_log.hex() + "\n")
                    except Exception as e:
                        print(f"Error decrypting log: {e}")
                        file.write(log)
            print("All logs have now been marked as checked.")
        else:
            print("No logs found.")
    
    def HasUncheckedSuspiciousLogs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                logs = file.readlines()
                for log in logs:
                    try:
                        decrypted_log = CryptoUtils.DecryptWithPrivateKey(self.private_key, bytes.fromhex(log.strip()))
                        log_parts = decrypted_log.strip().split('|')
                        if len(log_parts) > 5 and "Suspicious: True" in log_parts[5] and "Checked: False" in log_parts[6]:
                            return True
                    except Exception as e:
                        print(f"Error decrypting log: {e}")
        return False