from users import roles
from users import Service
from users import SystemAdministrator
from users import SuperAdministrator
from roles import roles
from cryptoUtils import CryptoUtils
import os
import time

class UI:
    def __init__(self) -> None:
        pass

    def DisplayLogo(self):
        ascii_art = """

$$\   $$\ $$$$$$$\  $$$$$$$\   $$$$$$\  $$\   $$\       $$\      $$\  $$$$$$\  $$$$$$$\  $$$$$$\ $$\       $$$$$$\ $$$$$$$$\ $$\     $$\ 
$$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$$\  $$ |      $$$\    $$$ |$$  __$$\ $$  __$$\ \_$$  _|$$ |      \_$$  _|\__$$  __|\$$\   $$  |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ /  $$ |$$$$\ $$ |      $$$$\  $$$$ |$$ /  $$ |$$ |  $$ |  $$ |  $$ |        $$ |     $$ |    \$$\ $$  / 
$$ |  $$ |$$$$$$$  |$$$$$$$\ |$$$$$$$$ |$$ $$\$$ |      $$\$$\$$ $$ |$$ |  $$ |$$$$$$$\ |  $$ |  $$ |        $$ |     $$ |     \$$$$  /  
$$ |  $$ |$$  __$$< $$  __$$\ $$  __$$ |$$ \$$$$ |      $$ \$$$  $$ |$$ |  $$ |$$  __$$\   $$ |  $$ |        $$ |     $$ |      \$$  /   
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\$$$ |      $$ |\$  /$$ |$$ |  $$ |$$ |  $$ |  $$ |  $$ |        $$ |     $$ |       $$ |    
\$$$$$$  |$$ |  $$ |$$$$$$$  |$$ |  $$ |$$ | \$$ |      $$ | \_/ $$ | $$$$$$  |$$$$$$$  |$$$$$$\ $$$$$$$$\ $$$$$$\    $$ |       $$ |    
 \______/ \__|  \__|\_______/ \__|  \__|\__|  \__|      \__|     \__| \______/ \_______/ \______|\________|\______|   \__|       \__|    
                                                                                                                                         
========================================================================================================================================
            """
        print(ascii_art)
    
    def ClearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def OptionMenu(self, user, db, loggingSys, backupSys):
        while user is not None:
            time.sleep(1)
            if isinstance(user, SuperAdministrator):
                self.ClearScreen()
                self.DisplayLogo()

                if not db.ValidateSession(user.id, user.session,user.role):
                    print("You will now be logged out of the system...")
                    loggingSys.Log("Logged out", True,"User ID associated with role Super Admin not found.",f"{user.userName}")
                    user = None
                    time.sleep(2)
                    break

                logoutResult = self.SuperAdminMenu(user, db, loggingSys, backupSys)
                if logoutResult is True:
                    db.ClearSession(user.id,user.session)
                    user = None
                    break

            elif isinstance(user, SystemAdministrator):
                self.ClearScreen()
                self.DisplayLogo()

                if not db.ValidateSession(user.id, user.session,user.role):
                    print("You will now be logged out of the system...")
                    loggingSys.Log("Logged out", False,"User ID associated with role Admin not found ",f"{user.userName}")
                    user = None
                    time.sleep(2)
                    break 

                logoutResult = self.SystemAdminMenu(user, db, loggingSys, backupSys)
                if logoutResult is True:
                    db.ClearSession(user.id,user.session)
                    user = None
                    break

            elif isinstance(user, Service):
                self.ClearScreen()
                self.DisplayLogo()

                if not db.ValidateSession(user.id, user.session,user.role):
                    print("You will now be logged out of the system...")
                    loggingSys.Log("Logged out", False,"User ID associated with role SERVICE not found (possibly due to a removal of their account during a backup restore.)",f"{user.userName}")
                    user = None
                    time.sleep(2)
                    break 

                logoutResult = self.ServiceMenu(user, db, loggingSys)
                if logoutResult is True:
                    db.ClearSession(user.id,user.session)
                    user = None
                    break

            else:
                print("Unauthorized access to menu!")
                loggingSys.Log("User tried to access options with invalid role.", True, username=user.userName)
                break

    def SuperAdminMenu(self,user,db,loggingSys,backupSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            "1": lambda : user.DisplayUsers(db),
            "2": lambda : user.UserCreation(db, roles.SERVICE,loggingSys),
            "3": lambda : user.EditUser(db,roles.SERVICE,loggingSys),
            "4": lambda : user.Deletion( db, roles.SERVICE, loggingSys),
            "5": lambda : user.ResetPassword(db,roles.SERVICE,loggingSys), 
            "6": lambda : user.UserCreation(db, roles.ADMIN,loggingSys),
            "7": lambda : user.EditUser(db,roles.ADMIN,loggingSys),
            "8": lambda : user.Deletion(db, roles.ADMIN, loggingSys),
            "9": lambda : user.ResetPassword(db,roles.ADMIN,loggingSys), 

            "10": lambda : user.CreateBackup(backupSys,loggingSys),
            "11": lambda : user.RestoreBackup(backupSys,loggingSys,db),
            "12": lambda : user.GenerateRestoreCode(db,backupSys,loggingSys),
            "13" : lambda : user.ManageRestoreCodes(db, loggingSys),
            '14': lambda : user.DisplayLogs(db,loggingSys),

            "15": lambda : user.CreateScooter(db, loggingSys),
            "16": lambda : user.EditScooter(db,loggingSys),
            "17": lambda : user.DeleteScooter(db,loggingSys),
            "18": lambda : user.SearchScooter(db,loggingSys),
                        
            "19": lambda : user.CreateTraveller(db,roles.SUPERADMIN,loggingSys),
            "20": lambda : user.EditTraveller(db,loggingSys),
            "21": lambda : user.DeleteTraveller(db,loggingSys),
            "22": lambda : user.SearchTraveller(db,loggingSys),
            }
        print("""
=====================================================
|    $$\      $$\ $$$$$$$$\ $$\   $$\ $$\   $$\     |
|    $$$\    $$$ |$$  _____|$$$\  $$ |$$ |  $$ |    |
|    $$$$\  $$$$ |$$ |      $$$$\ $$ |$$ |  $$ |    |
|    $$\$$\$$ $$ |$$$$$\    $$ $$\$$ |$$ |  $$ |    |
|    $$ \$$$  $$ |$$  __|   $$ \$$$$ |$$ |  $$ |    |
|    $$ |\$  /$$ |$$ |      $$ |\$$$ |$$ |  $$ |    |
|    $$ | \_/ $$ |$$$$$$$$\ $$ | \$$ |\$$$$$$  |    |
|    \__|     \__|\________|\__|  \__| \______/     |
=====================================================
User Management:
[1] - List all users and their roles
[2] - Add a new Service Engineer
[3] - Modify or update an existing Service Engineer’s account and profile
[4] - Delete an existing Service Engineer’s account
[5] - Reset an existing Service Engineer’s password (a temporary password)
[6] - Add a new System Administrator
[7] - Modify or update an existing System Administrator’s account and profile
[8] - Delete an existing System Administrator’s account
[9] - Reset an existing System Administrator’s password (a temporary password)    

System Management:
[10] - Make a backup of the system (members and users’ information, logs)
[11] - Restore a backup of the system    
[12] - Genereate a restore code for the system
[13] - Manage restore codes for the system  
[14] - See the logs file(s) of the system  

Scooter Management:
[15] - Add a new scooter to the system
[16] - Update a scooter's information
[17] - Delete a scooter's record from the database
[18] - Search for a scooter

Traveller Management:
[19] - Add a new traveller to the system
[20] - Modify or update the information of a traveller in the system
[21] - Delete a traveller's record from the database
[22] - Search and retrieve the information of a traveller  

[0] or [Q] - Quit
""")
        user.AlertLogs(loggingSys)
        input_ = input("Press a key:").strip().upper()
        if input_ in ['0', 'Q']:
            print("Logging out...")
            time.sleep(2)
            return True
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.ClearScreen()
                self.DisplayLogo()
                methodCall[input_.upper()]()
            else:
                loggingSys.Log("User gave an invalid option.",False,additional_info='Input was not in the list of options', username=user.userName)
                print("Invalid input given")
                time.sleep(1)
        else:
            loggingSys.Log("User gave an invalid option.",True, additional_info='Input was not a string instance.', username=user.userName)
            print("Invalid input given")
            time.sleep(1)

        return False 

    def SystemAdminMenu(self,user,db,loggingSys,backupSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            "1": lambda : user.ChangePassword(db,loggingSys), 
            "2": lambda : user.EditOwnAccount(db,loggingSys),
            "3": lambda : user.AccountDeletion(db, loggingSys),

            "4": lambda :  user.DisplayLogs(db,loggingSys),
            "5": lambda :  user.CreateBackup(backupSys,loggingSys), 
            "6": lambda : user.RestoreBackup(backupSys,loggingSys,db),

            "7": lambda : user.DisplayUsers(db),
            "8": lambda : user.UserCreation(db, roles.SERVICE,loggingSys),
            "9": lambda : user.EditUser(db,roles.SERVICE,loggingSys),
            "10": lambda : user.Deletion(db, roles.SERVICE, loggingSys),
            "11": lambda : user.ResetPassword(db,roles.SERVICE,loggingSys), 

            "15": lambda : user.CreateScooter(db, loggingSys),
            "16": lambda : user.EditScooter(db,loggingSys),
            "17": lambda : user.DeleteScooter(db,loggingSys),
            "18": lambda : user.SearchScooter(db,loggingSys),
                        
            "19": lambda : user.CreateTraveller(db,roles.ADMIN,loggingSys),
            "20": lambda : user.EditTraveller(db,loggingSys),
            "21": lambda : user.DeleteTraveller(db,loggingSys),
            "22": lambda : user.SearchTraveller(db,loggingSys),
        }


        print("""
=====================================================
|    $$\      $$\ $$$$$$$$\ $$\   $$\ $$\   $$\     |
|    $$$\    $$$ |$$  _____|$$$\  $$ |$$ |  $$ |    |
|    $$$$\  $$$$ |$$ |      $$$$\ $$ |$$ |  $$ |    |
|    $$\$$\$$ $$ |$$$$$\    $$ $$\$$ |$$ |  $$ |    |
|    $$ \$$$  $$ |$$  __|   $$ \$$$$ |$$ |  $$ |    |
|    $$ |\$  /$$ |$$ |      $$ |\$$$ |$$ |  $$ |    |
|    $$ | \_/ $$ |$$$$$$$$\ $$ | \$$ |\$$$$$$  |    |
|    \__|     \__|\________|\__|  \__| \______/     |
=====================================================
Account Management:
[1] - Update their own password
[2] - Edit own profile
[3] - Delete own account
              
System Management:
[4]- See the logs file(s) of the system
[5] - Make a backup of the system (members and users’ information, logs)
[6] - Restore a backup of the system      

User Management:
[7] - Get list of users and their roles
[8] - Add a new Service Engineer
[9] - Modify or update an existing Service Engineer’s account and profile
[10] - Delete an existing Service Engineer’s account
[11] - Reset an existing Service Engineer’s password (a temporary password)   
              
Scooter Management:
[12] - Search for a scooter
[13] - Add a new scooter to the system
[14] - Update a scooter's information
[15] - Delete a scooter's record from the database
              
Traveller Management:             
[16] - Add a new traveller to the system
[17] - Modify or update the information of a traveller in the system
[18] - Delete a traveller's record from the database
[19] - Search and retrieve the information of a traveller
              
[0] or [Q]- Quit
""")
        user.AlertLogs(loggingSys)
        input_ = input("Press a key:").strip().upper()
        if input_ in ['0', 'Q']:
            print("Logging out...")
            time.sleep(2)
            return True
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.ClearScreen()
                self.DisplayLogo()
                methodCall[input_.upper()]()
            else:
                loggingSys.Log("User gave an invalid option.",False,additional_info='Input was not in the list of options', username=user.userName)
                print("Invalid input given")
                time.sleep(1)
        else:
            loggingSys.Log("User gave an invalid option.",True, additional_info='Input was not a string instance.', username=user.userName)
            print("Invalid input given")
            time.sleep(1)
        
        return False

    def ServiceMenu(self,user,db,loggingSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            "1": lambda : user.ChangePassword(db,loggingSys), 
            "2": lambda : user.EditScooter(db,loggingSys),
            "3": lambda : user.SearchScooter(db,loggingSys),
        }


        print("""
=====================================================
|    $$\      $$\ $$$$$$$$\ $$\   $$\ $$\   $$\     |
|    $$$\    $$$ |$$  _____|$$$\  $$ |$$ |  $$ |    |
|    $$$$\  $$$$ |$$ |      $$$$\ $$ |$$ |  $$ |    |
|    $$\$$\$$ $$ |$$$$$\    $$ $$\$$ |$$ |  $$ |    |
|    $$ \$$$  $$ |$$  __|   $$ \$$$$ |$$ |  $$ |    |
|    $$ |\$  /$$ |$$ |      $$ |\$$$ |$$ |  $$ |    |
|    $$ | \_/ $$ |$$$$$$$$\ $$ | \$$ |\$$$$$$  |    |
|    \__|     \__|\________|\__|  \__| \______/     |
=====================================================
Account Management:
[1] - Update their own password
              
Scooter Management:
[2] - Update a scooter's information
[3] - Search for a scooter
              
[0] - [Q] Quit
""")
        input_ = input("Press a key:").strip().upper()
        if input_ in ['0', 'Q']:
            print("Logging out...")
            time.sleep(2)
            return True
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.ClearScreen()
                self.DisplayLogo()
                methodCall[input_.upper()]()
            else:
                loggingSys.Log("User gave an invalid option.",False,additional_info='Input was not in the list of options', username=user.userName)
                print("Invalid input given")
                time.sleep(1)
        else:
            loggingSys.Log("User gave an invalid option.",True, additional_info='Input was not a string instance.', username=user.userName)
            print("Invalid input given")
            time.sleep(1)
        
        return False