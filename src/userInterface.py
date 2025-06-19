from users import roles
from users import service
from users import systemAdministrator
from users import superAdministrator
from roles import roles
from cryptoUtils import cryptoUtils
import os
import time

class UI:
    def __init__(self) -> None:
        pass

    def displayLogo(self):
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
    
    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def optionMenu(self, user, db, loggingSys, backupSys):
        while user is not None:
            private_key = cryptoUtils.loadPrivateKey()
            time.sleep(1)
            if isinstance(user, superAdministrator):
                self.clearScreen()
                self.displayLogo()

                if not db.validateSession(user.id, user.session):
                    print("You will now be logged out of the system...")
                    loggingSys.log("Logged out", True,"User ID associated with role Super Admin not found.",f"{user.userName}")
                    user = None
                    time.sleep(2)
                    break

                logoutResult = self.superAdministrator_Menu(user, db, loggingSys, backupSys)
                if logoutResult is True:
                    user = None
                    break

            elif isinstance(user, systemAdministrator):
                self.clearScreen()
                self.displayLogo()

                if not db.validateSession(user.id, user.session):
                    print("You will now be logged out of the system...")
                    loggingSys.log("Logged out", False,"User ID associated with role Admin not found ",f"{user.userName}")
                    user = None
                    time.sleep(2)
                    break 

                logoutResult = self.systemAdministrator_Menu(user, db, loggingSys, backupSys)
                if logoutResult is True:
                    user = None
                    break

            elif isinstance(user, service):
                self.clearScreen()
                self.displayLogo()

                if not db.validateSession(user.id, user.session):
                    print("You will now be logged out of the system...")
                    loggingSys.log("Logged out", False,"User ID associated with role SERVICE not found (possibly due to a removal of their account during a backup restore.)",f"{user.userName}")
                    user = None
                    time.sleep(2)
                    break 

                logoutResult = self.service_Menu(user, db, loggingSys)
                if logoutResult is True:
                    user = None
                    break

            else:
                print("Unauthorized access to menu!")
                loggingSys.log("User tried to access options with invalid role.", True, username=user.userName)
                break

    def superAdministrator_Menu(self,user,db,loggingSys,backupSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            "1": lambda : user.displayUsers(db),
            "2": lambda : user.userCreation(db, roles.SERVICE,loggingSys),
            "3": lambda : user.editUser(user,db,roles.SERVICE,loggingSys),
            "4": lambda : user.deletion(user, db, roles.SERVICE, loggingSys),
            "5": lambda : user.resetPassword(user,db,roles.SERVICE,loggingSys), 
            "6": lambda : user.userCreation(db, roles.ADMIN,loggingSys),
            "7": lambda : user.editUser(user,db,roles.ADMIN,loggingSys),
            "8": lambda : user.deletion(user, db, roles.ADMIN, loggingSys),
            "9": lambda : user.resetPassword(user,db,roles.ADMIN,loggingSys), 
            "10": lambda : user.createBackup(user,backupSys,loggingSys),
            "11": lambda : user.restoreBackup(backupSys,loggingSys,db),
            "12": lambda : user.displayLogs(loggingSys),
            "13": lambda : user.createTraveller(db,roles.SUPERADMIN,loggingSys),
            "14": lambda : user.updateTraveller(db,loggingSys),
            "15": lambda : user.deletion(user, db, None, loggingSys),
            "16": lambda : user.memberSearch(db,loggingSys),
            "17": lambda : user.generateRestoreCode( db,backupSys,loggingSys),
            "18": lambda : user.createScooter(db, loggingSys),
            "19" : lambda : user.accountDeletion( db, loggingSys),
            "20" : lambda : user.manageRestoreCodes( db, loggingSys),
            'L': lambda : user.displayUsers(db),
            'AC': lambda : user.userCreation(db, roles.SERVICE,loggingSys),
            'UC': lambda : user.editUser(user,db,roles.SERVICE,loggingSys),
            'DC': lambda : user.deletion(user, db, roles.SERVICE, loggingSys),
            'RC': lambda : user.resetPassword(user,db,roles.SERVICE,loggingSys),
            'AA': lambda : user.userCreation(db, roles.ADMIN,loggingSys),
            'UA': lambda : user.editUser(user,db,roles.ADMIN,loggingSys),
            'DA': lambda : user.deletion(user, db, roles.ADMIN, loggingSys),
            'RA': lambda : user.resetPassword(user,db,roles.ADMIN,loggingSys), 
            'BA': lambda : user.createBackup(user,backupSys,loggingSys),
            'RB': lambda : user.restoreBackup(backupSys,loggingSys,db),
            'SL': lambda : user.displayLogs(loggingSys),
            'AM': lambda : user.memberCreation(db,loggingSys),
            'UM': lambda : user.editMember(db,loggingSys),
            'DM': lambda : user.deletion(user, db, None, loggingSys),
            'SM': lambda : user.memberSearch(db,loggingSys),
            'MR': lambda : user.generateRestoreCode( db,backupSys,loggingSys)
            }
        print("""
Super Admin Menu:
[1] or [L] - Get list of users and their roles
[2] or [AC] - Add a new SERVICE
[3] or [UC] - Update an existing SERVICE’s account and profile
[4] or [DC] - Delete an existing SERVICE’s account
[5] or [RC] - Reset an existing SERVICE’s password
[6] or [AA] - Add a new admin
[7] or [UA] - Update an existing admin’s account and profile
[8] or [DA] - Delete an existing admin’s account
[9] or [RA] - Reset an existing admin’s password
[10] or [BA] - Make a backup of the system
[11] or [RB] - Restore a backup of the system
[12] or [SL] - See the logs file of the system
[13] or [AM] - Add a new traveller
[14] or [UM] - Update a member’s information
[15] or [DM] - Delete a member’s record
[16] or [SM] - Search and retrieve a member’s information
[17] or [MR] - Generate a restore code for the system
              18 add scooter
[0] or [Q] - Quit
""")
        user.alertLogs(loggingSys)
        input_ = input("Press a key:").strip().upper()
        if input_ in ['0', 'Q']:
            print("Logging out...")
            time.sleep(2)
            return True
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[input_.upper()]()
            else:
                loggingSys.log("User gave an invalid option.",False,additional_info='Input was not in the list of options', username=user.userName)
                print("Invalid input given")
                time.sleep(1)
        else:
            loggingSys.log("User gave an invalid option.",True, additional_info='Input was not a string instance.', username=user.userName)
            print("Invalid input given")
            time.sleep(1)

        return False 

    def systemAdministrator_Menu(self,user,db,loggingSys,backupSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            "1": lambda : user.changePassword(user,db,loggingSys), 
            "2": lambda : user.displayUsers(db), 
            "3": lambda : user.accountDeletion(db, loggingSys),
            "4": lambda : user.editUser(user,db,roles.SERVICE,loggingSys),
            "5": lambda : user.deletion(user, db, roles.SERVICE, loggingSys), 
            "6": lambda : user.resetPassword(user,db,roles.SERVICE,loggingSys), 
            "7": lambda :  user.createBackup(user,backupSys,loggingSys), 
            "8": lambda :  user.displayLogs(loggingSys),
            "9": lambda : user.memberCreation(db,loggingSys), 
            "10": lambda : user.editMember(db,loggingSys), 
            "11": lambda : user.deletion(user, db, None, loggingSys), 
            "12": lambda : user.memberSearch(db,loggingSys),
            "13": lambda : user.restoreBackup(backupSys,loggingSys,db),
            "14": lambda : user.createScooter(db, loggingSys)
        }


        print("""
System Administrator Menu:
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
              
[0] or [Q] - Quit
""")
        user.alertLogs(loggingSys)
        input_ = input("Press a key:").strip().upper()
        if input_ in ['0', 'Q']:
            print("Logging out...")
            time.sleep(2)
            return True
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[input_.upper()]()
            else:
                loggingSys.log("User gave an invalid option.",False,additional_info='Input was not in the list of options', username=user.userName)
                print("Invalid input given")
                time.sleep(1)
        else:
            loggingSys.log("User gave an invalid option.",True, additional_info='Input was not a string instance.', username=user.userName)
            print("Invalid input given")
            time.sleep(1)
        
        return False

    def service_Menu(self,user,db,loggingSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            "1": lambda : user.changePassword(user,db,loggingSys), 
        }


        print("""
SERVICE Menu:
Account Management:
[1] or [UP] - Update their own password
              
Scooter Management:
[2] or [US] - Update a scooter's information
[3] or [SS] - Search for a scooter
""")
        input_ = input("Press a key:").strip().upper()
        if input_ in ['0', 'Q']:
            print("Logging out...")
            time.sleep(2)
            return True
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[input_.upper()]()
            else:
                loggingSys.log("User gave an invalid option.",False,additional_info='Input was not in the list of options', username=user.userName)
                print("Invalid input given")
                time.sleep(1)
        else:
            loggingSys.log("User gave an invalid option.",True, additional_info='Input was not a string instance.', username=user.userName)
            print("Invalid input given")
            time.sleep(1)
        
        return False