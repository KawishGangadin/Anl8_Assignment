import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_format = '%(log_number)s | %(asctime)s | %(username)s | %(activity)s | %(additional_info)s | Suspicious: %(suspicious)s | Checked: %(checked)s | %(message)s'
        self.log_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.log_dir, 'logs', 'uniquemeal.log')  # Absolute path to the log file
        self.check_create_log_file()  # Create the log file if it doesn't exist
        self.basicConfig()  # Configure logging

    def basicConfig(self):
        logging.basicConfig(filename=self.log_file, filemode='a', level=logging.INFO, format=self.log_format, datefmt='%Y-%m-%d %H:%M:%S')

    def log(self, activity, suspicious=False, additional_info='-', username='no username'):
        logging.info(
            '',
            extra={
                'log_number': self.get_next_log_number(),
                'username': username,
                'activity': activity,
                'additional_info': additional_info,
                'suspicious': suspicious,
                'checked': False
            }
        )

    def check_create_log_file(self):
        # Ensure the log directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        # Create an empty log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'):
                pass

    def get_next_log_number(self):
        # Here you can implement logic to get the next log number from a database or file
        # For now, returning a static value
        return 1
