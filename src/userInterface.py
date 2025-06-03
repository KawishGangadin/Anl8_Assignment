from users import roles
from users import consultant
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
 _   _       _                    __  __            _ 
| | | |_ __ (_) __ _ _   _  ___  |  \/  | ___  __ _| |
| | | | '_ \| |/ _` | | | |/ _ \ | |\/| |/ _ \/ _` | |
| |_| | | | | | (_| | |_| |  __/ | |  | |  __/ (_| | |
 \___/|_| |_|_|\__, |\__,_|\___| |_|  |_|\___|\__,_|_|
                  |_|                                 
=======================================================
            """
        print(ascii_art)
    
    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def optionMenu(self, user, db, loggingSys, backupSys):
        while user is not None:  # Loop while the user is logged in
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
                    break  # Exit the loop to log out
                # Only return None if the user logs out

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
                 # Exit the loop to log out
                logoutResult = self.systemAdministrator_Menu(user, db, loggingSys, backupSys)
                if logoutResult is True:
                    user = None
                    break

            elif isinstance(user, consultant):
                self.clearScreen()
                self.displayLogo()

                if not db.validateSession(user.id, user.session):
                    print("You will now be logged out of the system...")
                    loggingSys.log("Logged out", False,"User ID associated with role Consultant not found (possibly due to a removal of their account during a backup restore.)",f"{user.userName}")
                    user = None
                    time.sleep(2)
                    break  # Exit the loop to log out

                logoutResult = self.consultant_Menu(user, db, loggingSys)
                if logoutResult is True:
                    user = None
                    break

            else:
                print("Unauthorized access to menu!")
                loggingSys.log("User tried to access options with invalid role.", True, username=user.userName)
                break  # exit

    def superAdministrator_Menu(self,user,db,loggingSys,backupSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            "1": lambda : user.displayUsers(db),
            "2": lambda : user.userCreation(db, roles.CONSULTANT,loggingSys),
            "3": lambda : user.editUser(user,db,roles.CONSULTANT,loggingSys),
            "4": lambda : user.deletion(user, db, roles.CONSULTANT, loggingSys),
            "5": lambda : user.resetPassword(user,db,roles.CONSULTANT,loggingSys), 
            "6": lambda : user.userCreation(db, roles.ADMIN,loggingSys),
            "7": lambda : user.editUser(user,db,roles.ADMIN,loggingSys),
            "8": lambda : user.deletion(user, db, roles.ADMIN, loggingSys),
            "9": lambda : user.resetPassword(user,db,roles.ADMIN,loggingSys), 
            "10": lambda : user.createBackup(user,backupSys,loggingSys),
            "11": lambda : user.restoreBackup(backupSys,loggingSys,db),
            "12": lambda : user.displayLogs(loggingSys),
            "13": lambda : user.createTraveller(db,roles.SUPERADMIN,loggingSys),
            "14": lambda : user.editMember(db,loggingSys),
            "15": lambda : user.deletion(user, db, None, loggingSys),
            "16": lambda : user.memberSearch(db,loggingSys),
            "17": lambda : user.generateRestoreCode( db, loggingSys),
            'L': lambda : user.displayUsers(db),
            'AC': lambda : user.userCreation(db, roles.CONSULTANT,loggingSys),
            'UC': lambda : user.editUser(user,db,roles.CONSULTANT,loggingSys),
            'DC': lambda : user.deletion(user, db, roles.CONSULTANT, loggingSys),
            'RC': lambda : user.resetPassword(user,db,roles.CONSULTANT,loggingSys),
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
            'MR': lambda : user.generateRestoreCode( db, loggingSys)
            }
        print("""
Super Admin Menu:
[1] or [L] - Get list of users and their roles
[2] or [AC] - Add a new consultant
[3] or [UC] - Update an existing consultant’s account and profile
[4] or [DC] - Delete an existing consultant’s account
[5] or [RC] - Reset an existing consultant’s password
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
            "3": lambda : user.userCreation(db, roles.CONSULTANT,loggingSys), 
            "4": lambda : user.editUser(user,db,roles.CONSULTANT,loggingSys),
            "5": lambda : user.deletion(user, db, roles.CONSULTANT, loggingSys), 
            "6": lambda : user.resetPassword(user,db,roles.CONSULTANT,loggingSys), 
            "7": lambda :  user.createBackup(user,backupSys,loggingSys), 
            "8": lambda :  user.displayLogs(loggingSys),
            "9": lambda : user.memberCreation(db,loggingSys), 
            "10": lambda : user.editMember(db,loggingSys), 
            "11": lambda : user.deletion(user, db, None, loggingSys), 
            "12": lambda : user.memberSearch(db,loggingSys),
            "13": lambda : user.restoreBackup(backupSys,loggingSys,db),
            'UP': lambda : user.changePassword(user,db,loggingSys), 
            'LU': lambda : user.displayUsers(db), 
            'AC': lambda : user.userCreation(db, roles.CONSULTANT,loggingSys), 
            'UC': lambda : user.editUser(user,db,roles.CONSULTANT,loggingSys),
            'DC': lambda : user.deletion(user, db, roles.CONSULTANT, loggingSys), 
            'RC': lambda : user.resetPassword(user,db,roles.CONSULTANT,loggingSys),  
            'MB': lambda : user.createBackup(user,backupSys,loggingSys),
            'SL': lambda : user.displayLogs(loggingSys),
            'AM': lambda : user.memberCreation(db,loggingSys), 
            'UM': lambda : user.editMember(db,loggingSys), 
            'DM': lambda : user.deletion(user, db, None, loggingSys), 
            'SM': lambda : user.memberSearch(db,loggingSys),
            'RB': lambda : user.restoreBackup(backupSys,loggingSys,db)
        }


        print("""
System Administrator Menu:
[1] or [UP] - Update their own password
[2] or [LU] - Check the list of users and their roles
[3] or [AC] - Define and add a new consultant to the system
[4] or [UC] - Modify or update an existing consultant’s account and profile
[5] or [DC] - Delete an existing consultant’s account
[6] or [RC] - Reset an existing consultant’s password (a temporary password)
[7] or [MB] - Make a backup of the system (members and users’ information, logs)
[8] or [SL] - See the logs file(s) of the system
[9] or [AM] - Add a new member to the system
[10] or [UM] - Modify or update the information of a member in the system
[11] or [DM] - Delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information)
[12] or [SM] - Search and retrieve the information of a member
[13] or [RB] - Restore a backup of the system
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

    def consultant_Menu(self,user,db,loggingSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            "1": lambda : user.changePassword(user,db,loggingSys), 
            "2": lambda : user.memberCreation(db,loggingSys), 
            "3": lambda : user.editMember(db,loggingSys), 
            "4": lambda : user.memberSearch(db,loggingSys),
            'UP': lambda : user.changePassword(user,db,loggingSys), 
            'AM': lambda : user.memberCreation(db,loggingSys), 
            'UM': lambda : user.editMember(db,loggingSys), 
            'SM': lambda : user.memberSearch(db,loggingSys),
        }


        print("""
Consultant Menu:
[1] or [UP] - Update their own password
[2] or [AM] - Add a new member to the system
[3] or [UM] - Modify or update the information of a member in the system
[4] or [SM] - Search and retrieve the information of a member
[0] or [Q] - Quit
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