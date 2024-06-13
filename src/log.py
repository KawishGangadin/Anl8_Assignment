import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_format = '%(log_number)s | %(asctime)s | %(username)s | %(activity)s | %(additional_info)s | Suspicious: %(suspicious)s | Checked: %(checked)s | %(message)s'
        self.log_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.log_dir, 'logs', 'uniquemeal.log')  # Absolute path to the log file
        self.checkLogFile()  # Create the log file if it doesn't exist
        self.basicConfig()  # Configure logging

    def basicConfig(self):
        logging.basicConfig(filename=self.log_file, filemode='a', level=logging.INFO, format=self.log_format, datefmt='%Y-%m-%d %H:%M:%S')

    def log(self, activity, suspicious=False, additional_info='-', username='no username'):
        logging.info(
            '',
            extra={
                'log_number': self.nextNumber(),
                'username': username,
                'activity': activity,
                'additional_info': additional_info,
                'suspicious': suspicious,
                'checked': False
            }
        )


    def checkLogFile(self):
        # Ensure the log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        # Create an empty log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'):
                pass


    def nextNumber(self):
            # Count the number of lines in the log file to determine the next log number
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as file:
                    lines = file.readlines()
                    return len(lines) + 1
            return 1
    
    def printLogs(self):
        # Print all logs in the log file
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                logs = file.readlines()
                for log in logs:
                    print(log.strip())
            self.markLogs()
        else:
            print("No logs found.")

    def markLogs(self):
    # Mark all logs as checked that aren't already marked
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                logs = file.readlines()
            
            with open(self.log_file, 'w') as file:
                for log in logs:
                    log_parts = log.strip().split('|')
                    if len(log_parts) > 6 and "Checked: False" in log_parts[6]:
                        log_parts[6] = "Checked: True"
                    file.write('|'.join(log_parts) + "\n")
            print("All logs have now been marked as checked.")
        else:
            print("No logs found.")
