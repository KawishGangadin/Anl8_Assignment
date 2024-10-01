import os
import zipfile
import logging
import time
from users import systemAdministrator, superAdministrator

class backup:
    def __init__(self):
        self.backupDir = os.path.dirname(os.path.abspath(__file__))
        self.backupFolder = os.path.join(self.backupDir, 'backups')
        self.logsFolder = os.path.join(self.backupDir, 'logs')
        self.log_format = '%(log_number)s | %(asctime)s | %(username)s | %(activity)s | %(additional_info)s | Suspicious: %(suspicious)s | Checked: %(checked)s | %(message)s'

    def createBackupZip(self, user):
        if isinstance(user, (systemAdministrator, superAdministrator)):
            logsFolder = self.logsFolder
            
            # Generate unique backup name
            backupName = f"backup{self.countBackups()}.zip"
            
            # Check if the backup folder exists or create it if it doesn't
            if not os.path.exists(self.backupFolder):
                os.makedirs(self.backupFolder)
            
            # Check if the logs folder exists
            if not os.path.exists(logsFolder):
                raise FileNotFoundError(f"Logs folder '{logsFolder}' does not exist")
            
            logFile = 'uniquemeal.log'
            dbFile = 'uniqueMeal.db'
            
            logPath = os.path.join(logsFolder, logFile)
            dbPath = os.path.join(self.backupDir, dbFile)
            
            # Check if both files exist
            if not os.path.exists(logPath):
                raise FileNotFoundError(f"{logFile} does not exist in the logs folder")
            if not os.path.exists(dbPath):
                raise FileNotFoundError(f"{dbFile} does not exist in the current directory")
            
            # If backupName already exists, find a unique name
            if os.path.exists(os.path.join(self.backupFolder, backupName)):
                backupCount = 1
                while True:
                    newBackupName = f"backup{backupCount}.zip"
                    if not os.path.exists(os.path.join(self.backupFolder, newBackupName)):
                        backupName = newBackupName
                        break
                    backupCount += 1
            
            # Create the zip file
            zipFilePath = os.path.join(self.backupFolder, backupName)
            with zipfile.ZipFile(zipFilePath, 'w') as backupZip:
                backupZip.write(logPath, os.path.basename(logPath))
                backupZip.write(dbPath, os.path.basename(dbPath))
            
            print(f"Backup created at {zipFilePath}")
        else:
            print("Unauthorized access...")

    def countBackups(self):
        if not os.path.exists(self.backupFolder):
            return 1 
        
        files = os.listdir(self.backupFolder)
        numBackups = len([file for file in files if file.endswith('.zip')])
        
        # If no backups exist, return 1
        if numBackups == 0:
            return 1
        
        return numBackups + 1
    
    def restoreBackup(self, backupName):
        # Shutdown logging to release any file locks
        logging.shutdown()
        backupFilePath = os.path.join(self.backupFolder, backupName)

        if not os.path.exists(backupFilePath):
            print(f"Backup file '{backupName}' does not exist.")
            return
        
        # Backup exists, proceed with restoration
        try:
            # Extract backup file to the backups folder
            with zipfile.ZipFile(backupFilePath, 'r') as backupZip:
                backupZip.extractall(self.backupFolder)
            
            print("Backup extracted successfully.")
            
            # Define file paths after extraction
            logFile = 'uniquemeal.log'
            dbFile = 'uniqueMeal.db'
            
            backupLogPath = os.path.join(self.backupFolder, logFile)
            backupDbPath = os.path.join(self.backupFolder, dbFile)
            
            # Remove original logs if they exist and move restored logs
            if os.path.exists(os.path.join(self.logsFolder, logFile)):
                os.remove(os.path.join(self.logsFolder, logFile))
                print(f"Removed existing '{os.path.join(self.logsFolder, logFile)}'")
            self.move_file(backupLogPath, os.path.join(self.logsFolder, logFile))
            
            # Remove original db if it exists and move restored db
            if os.path.exists(os.path.join(self.backupDir, dbFile)):
                os.remove(os.path.join(self.backupDir, dbFile))
                print(f"Removed existing '{os.path.join(self.backupDir, dbFile)}'")
            self.move_file(backupDbPath, os.path.join(self.backupDir, dbFile))
            
            print("Restoration complete.")
            time.sleep(2)
            
        except Exception as e:
            print(f"Error during restoration: {e}")
        
        # Reinitialize logging after restoration if needed
        logging.basicConfig(filename=os.path.join(self.logsFolder, logFile), filemode='a', level=logging.INFO, format=self.log_format, datefmt='%Y-%m-%d %H:%M:%S')

    def move_file(self, source_file, destination_file):
        try:
            if os.path.exists(destination_file):
                os.remove(destination_file)
            os.replace(source_file, destination_file)
            print(f"Successfully moved '{source_file}' to '{destination_file}'")
        except Exception as e:
            print(f"Error moving '{source_file}' to '{destination_file}': {e}")
    
    def listBackupNames(self):
        if not os.path.exists(self.backupFolder):
            print("No backups found.")
            return
        
        files = os.listdir(self.backupFolder)
        backupNames = [file for file in files if file.endswith('.zip')]
        
        if not backupNames:
            print("No backup files (.zip) found.")
        else:
            print("List of backup files:")
            for name in backupNames:
                print(name)
