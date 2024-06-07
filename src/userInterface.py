from users import roles
from users import consultant
from users import systemAdministrator
from users import superAdministrator
from users import roles
import os
import time

class UI:
    def __init__(self) -> None:
        pass
    
    def func1(self,db):
        print("Welcome to function 1")

    def func2(self,db):
        print("Welcome to function 2")

    def func3(self,db):
        print("Welcome to function 3")

    def func4(self,db):
        print("Welcome to function 4")

    def func5(self,db):
        print("Welcome to function 5")

    def func6(self,db):
        print("Welcome to function 6")

    def func7(self,db):
        print("Welcome to function 7")

    def func8(self,db):
        print("Welcome to function 8")

    def func9(self,db):
        print("Welcome to function 9")

    def func10(self,db):
        print("Welcome to function 10")

    def func11(self,db):
        print("Welcome to function 11")

    def func12(self,db):
        print("Welcome to function 12")

    def func13(self,db):
        print("Welcome to function 13")

    def func14(self,db):
        print("Welcome to function 14")

    def func15(self,db):
        print("Welcome to function 15")

    def func16(self,db):
        print("Welcome to function 16")

    def displayLogo(self):
        ascii_art = """
$$\   $$\           $$\                                     $$\      $$\                     $$\ 
$$ |  $$ |          \__|                                    $$$\    $$$ |                    $$ |
$$ |  $$ |$$$$$$$\  $$\  $$$$$$\  $$\   $$\  $$$$$$\        $$$$\  $$$$ | $$$$$$\   $$$$$$\  $$ |
$$ |  $$ |$$  __$$\ $$ |$$  __$$\ $$ |  $$ |$$  __$$\       $$\$$\$$ $$ |$$  __$$\  \____$$\ $$ |
$$ |  $$ |$$ |  $$ |$$ |$$ /  $$ |$$ |  $$ |$$$$$$$$ |      $$ \$$$  $$ |$$$$$$$$ | $$$$$$$ |$$ |
$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$   ____|      $$ |\$  /$$ |$$   ____|$$  __$$ |$$ |
\$$$$$$  |$$ |  $$ |$$ |\$$$$$$$ |\$$$$$$  |\$$$$$$$\       $$ | \_/ $$ |\$$$$$$$\ \$$$$$$$ |$$ |
\______/ \__|  \__|\__| \____$$ | \______/  \_______|      \__|     \__| \_______| \_______|\__|
                            $$ |                                                               
                            $$ |                                                               
                            \__|
==================================================================================================
            """
        print(ascii_art)
    
    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def optionMenu(self,user,db,loggingSys):
        while True:
            time.sleep(1)
            print(type(user))
            if isinstance(user, superAdministrator):
                self.clearScreen()
                self.displayLogo()
                self.superAdministrator_Menu(user,db,loggingSys)
            elif isinstance(user,systemAdministrator):
                self.clearScreen()
                self.displayLogo()
                self.systemAdministrator_Menu(user,db,loggingSys)
            elif isinstance(user,consultant):
                self.clearScreen()
                self.displayLogo()
                self.consultant_Menu(user,db,loggingSys)
            else:
                print("Unauthorized access to menu!")
                loggingSys.log("User tried to access options without proper access.",True)

    def superAdministrator_Menu(self,user,db,loggingSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            1: lambda : user.displayUsers(db),
            2: lambda : user.userCreation(db, roles.CONSULTANT,loggingSys),
            3: lambda : user.editUser(user,db,roles.CONSULTANT),
            4: lambda : self.func4(db),
            5: lambda : self.func5(db),
            6: lambda : user.userCreation(db, roles.ADMIN,loggingSys),
            7: lambda : user.editUser(user,db,roles.ADMIN),
            8: lambda : self.func8(db),
            9: lambda : self.func9(db),
            10: lambda : self.func10(db),
            11: lambda : self.func11(db),
            12: lambda : self.func12(db),
            13: lambda : self.func13(db),
            14: lambda : self.func14(db),
            15: lambda : self.func15(db),
            16: lambda : self.func16(db),
            'L': lambda : user.displayUsers(db),
            'AC': lambda : user.userCreation(db, roles.CONSULTANT,loggingSys),
            'UC': lambda : user.editUser(user,db,roles.CONSULTANT),
            'DC': lambda : self.func4(db),
            'RC': lambda : self.func5(db),
            'AA': lambda : user.userCreation(db, roles.ADMIN,loggingSys),
            'UA': lambda : user.editUser(user,db,roles.ADMIN),
            'DA': lambda : self.func8(db),
            'RA': lambda : self.func9(db),
            'BA': lambda : self.func10(db),
            'RB': lambda : self.func11(db),
            'SL': lambda : self.func12(db),
            'AM': lambda : self.func13(db),
            'UM': lambda : self.func14(db),
            'DM': lambda : self.func15(db),
            'SM': lambda : self.func16(db),
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
[13] or [AM] - Add a new member
[14] or [UM] - Update a member’s information
[15] or [DM] - Delete a member’s record
[16] or [SM] - Search and retrieve a member’s information
[0] or [Q] - Quit
""")
        input_ = input("Press a key:").strip().upper()
        if input_ in ['0', 'Q']:
            print("Exiting by choice...")
            exit()
        elif input_.isdigit():
            if int(input_) in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[int(input_)]()
            else:
                print("Invalid input given")
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[input_.upper()]()
            else:
                loggingSys.log("User gave an invalid option.",False)
                print("Invalid input given")
                time.sleep(1)
        else:
            loggingSys.log("User gave an invalid option.",True)
            print("Invalid input given")
            time.sleep(1)

    
    
    
    
    def systemAdministrator_Menu(self,user,db,loggingSys):
        print(f"Welcome {user.userName}")
        methodCall = {
            1: lambda : self.func1(db), 
            2: lambda : user.displayUsers(db), 
            3: lambda : self.func3(db), 
            4: lambda : user.editUser(user, db, roles.CONSULTANT),
            5: lambda : self.func5(db), 
            6: lambda : self.func6(db), 
            7: lambda : self.func7(db), 
            8: lambda : self.func8(db),
            9: lambda : self.func9(db), 
            10: lambda : self.func10(db), 
            11: lambda : self.func11(db), 
            12: lambda : self.func12(db),
            'UP': lambda : self.func1(db), 
            'LU': lambda : user.displayUsers(db), 
            'AC': lambda : self.func3(db), 
            'UC': lambda : user.editUser(user, db, roles.CONSULTANT),
            'DC': lambda : self.func5(db), 
            'RC': lambda : self.func6(db), 
            'MB': lambda : self.func7(db), 
            'SL': lambda : self.func8(db),
            'AM': lambda : self.func9(db), 
            'UM': lambda : self.func10(db), 
            'DM': lambda : self.func11(db), 
            'SM': lambda : self.func12(db),
        }


        print("""
System Administrator Menu:
[1] or [UP] - Update their own password
[2] or [LU] - Check the list of users and their roles
[3] or [AC] - Define and add a new consultant to the system
[4] or [UC] - Modify or update an existing consultant’s account and profile
[5] or [DC] - Delete an existing consultant’s account
[6] or [RC] - Reset an existing consultant’s password (a temporary password)
[7] or [MB] - Make a backup of the system and restore a backup (members information and users’ data)
[8] or [SL] - See the logs file(s) of the system
[9] or [AM] - Add a new member to the system
[10] or [UM] - Modify or update the information of a member in the system
[11] or [DM] - Delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information)
[12] or [SM] - Search and retrieve the information of a member
[0] or [Q] - Quit
""")

        input_ = input("Press a key:").strip().upper()
        if input_ in ['0', 'Q']:
            print("Exiting by choice...")
            exit()
        elif input_.isdigit():
            if int(input_) in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[int(input_)]()
            else:
                print("Invalid input given")
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[input_.upper()]()
            else:
                loggingSys.log("User gave an invalid option.",False)
                print("Invalid input given")
                time.sleep(1)
        else:
            loggingSys.log("User gave an invalid option.",True)
            print("Invalid input given")
            time.sleep(1)



    def consultant_Menu(self,user,db,loggingSys):
        print("Consultant Menu")