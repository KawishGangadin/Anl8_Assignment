from users import roles
from users import consultant
from users import systemAdministrator
from users import superAdministrator
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
        print("\033c", end="")

    def optionMenu(self,user,db):
        while True:
            time.sleep(1)
            print(type(user))
            if isinstance(user, systemAdministrator):
                self.clearScreen()
                self.displayLogo()
                self.systemAdministrator_Menu(user,db)
            elif isinstance(user,systemAdministrator):
                self.clearScreen()
                self.displayLogo()
                self.systemAdministrator_Menu(user,db)
            elif isinstance(user,consultant):
                self.clearScreen()
                self.displayLogo()
                self.systemAdministrator_Menu(user,db)
            else:
                print("Unauthorized access to menu!")

    def superAdministrator_Menu(self,user,db):
        print(f"Welcome {user.userName}")
        methodCall = {
            1: user.displayUsers, 2: self.func2, 3: self.func3, 4: self.func4,
            5: self.func5, 6: self.func6, 7: self.func7, 8: self.func8,
            9: self.func9, 10: self.func10, 11: self.func11, 12: self.func12,
            13: self.func13, 14: self.func14, 15: self.func15, 16: self.func16,
            'L': user.displayUsers, 'AC': self.func2, 'UC': self.func3, 'DC': self.func4,
            'RC': self.func5, 'AA': self.func6, 'UA': self.func7, 'DA': self.func8,
            'RA': self.func9, 'BA': self.func10, 'RB': self.func11, 'SL': self.func12,
            'AM': self.func13, 'UM': self.func14, 'DM': self.func15, 'SM': self.func16,
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
                methodCall[int(input_)](db)
            else:
                print("Invalid input given")
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[input_.upper()](db)
            else:
                print("Invalid input given")
                print("Exiting not by choice...")
                exit()
        else:
            print("Exiting...")
            print("Invalid input given")
            exit()

    def systemAdministrator_Menu(self,user,db):
        print(f"Welcome {user.userName}")
        methodCall = {
            1: self.func1, 2: user.displayUsers, 3: self.func3, 4: self.func4,
            5: self.func5, 6: self.func6, 7: self.func7, 8: self.func8,
            9: self.func9, 10: self.func10, 11: self.func11, 12: self.func12,
            'UP': self.func1, 'LU': user.displayUsers, 'AC': self.func3, 'UC': self.func4,
            'DC': self.func5, 'RC': self.func6, 'MB': self.func7, 'SL': self.func8,
            'AM': self.func9, 'UM': self.func10, 'DM': self.func11, 'SM': self.func12,}

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
                methodCall[int(input_)](db)
            else:
                print("Invalid input given")
        elif isinstance(input_.upper(),str):
            if input_.upper() in methodCall:
                self.clearScreen()
                self.displayLogo()
                methodCall[input_.upper()](db)
            else:
                print("Invalid input given")
                print("Exiting not by choice...")
                exit()
        else:
            print("Exiting...")
            print("Invalid input given")
            exit()
