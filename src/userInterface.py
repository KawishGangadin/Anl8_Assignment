from users import roles
from users import consultant
from users import systemAdministrator
from users import superAdministrator
import time

class UI:
    def __init__(self) -> None:
        pass
    
    def func1(self):
        print("Welcome to function 1")

    def func2(self):
        print("Welcome to function 2")

    def func3(self):
        print("Welcome to function 3")

    def func4(self):
        print("Welcome to function 4")

    def func5(self):
        print("Welcome to function 5")

    def func6(self):
        print("Welcome to function 6")

    def func7(self):
        print("Welcome to function 7")

    def func8(self):
        print("Welcome to function 8")

    def func9(self):
        print("Welcome to function 9")

    def func10(self):
        print("Welcome to function 10")

    def func11(self):
        print("Welcome to function 11")

    def func12(self):
        print("Welcome to function 12")

    def func13(self):
        print("Welcome to function 13")

    def func14(self):
        print("Welcome to function 14")

    def func15(self):
        print("Welcome to function 15")

    def func16(self):
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
                self.superAdministrator_Menu(user,db)
            else:
                print("not welcome")

    def superAdministrator_Menu(self,user,db):
        print(f"Welcome {user.userName}")
        optionsNum = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        optionsStr = ["l", "ac", "uc", "dc", "rc", "aa", "ua", "da", "ra", "ba", "rb", "sl", "am", "um", "dm", "sm", "q"]
        methodCallNum = {
            1: self.func1, 2: self.func2, 3: self.func3, 4: self.func4,
            5: self.func5, 6: self.func6, 7: self.func7, 8: self.func8,
            9: self.func9, 10: self.func10, 11: self.func11, 12: self.func12,
            13: self.func13, 14: self.func14, 15: self.func15, 16: self.func16,
        }

        methodCallStr = {
            'l': self.func1, 'ac': self.func2, 'uc': self.func3, 'dc': self.func4,
            'rc': self.func5, 'aa': self.func6, 'ua': self.func7, 'da': self.func8,
            'ra': self.func9, 'ba': self.func10, 'rb': self.func11, 'sl': self.func12,
            'am': self.func13, 'um': self.func14, 'dm': self.func15, 'sm': self.func16,
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
        elif input_ in optionsNum or input_.lower() in optionsStr:
            if input_.isdigit():
                if int(input_) in optionsNum:
                    methodCallNum[int(input_)]()
                else:
                    print("Invalid input given")
            else:
                if input_.lower() in optionsStr:
                    methodCallStr[input_.lower()]()
                else:
                    print("Invalid input given")
            print("Exiting not by choice...")
            exit()
        else:
            print("Exiting...")
            print("Invalid input given")
            exit()