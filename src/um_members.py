from userInterface import UI
import os
from database import DB
from log import Logger
from checkSum import Checksum
from auth import loginAuth
from inputValidation import Validation
from backup import backup
import time

def main():
    def initDB():
        dbPath = os.path.join(os.path.dirname(__file__), 'uniqueMeal.db')
        dbInitialization = DB(dbPath)
        dbInitialization.create_members_table()
        dbInitialization.create_users_table()
        dbInitialization.init_superadmin()
    initDB()

    running = True
    loggedIn = False
    attemptedUsernames = []
    attemptedPasswords = []
    userInterface = UI()

    dbPath = os.path.join(os.path.dirname(__file__), 'uniqueMeal.db')
    dataBase = DB(dbPath)
    loggingSys = Logger()
    backupSys = backup()
    logIn_System = loginAuth(dataBase)

    while running:
        maxTries = 3
        while not loggedIn:
            if maxTries <= 0:
                if len(set(attemptedPasswords)) > 1 and len(set(attemptedUsernames)) > 1:
                    print("Multiple usernames and passwords are tried wrong in a row")
                    loggingSys.log("Multiple usernames and passwords are tried wrong in a row", "True")
                    print("Exiting...")
                    exit()
                else:
                    print("A user tried to log into the system too many times with the wrong credentials")
                    loggingSys.log("A user tried to log into the system too many times with the wrong credentials", "True")
                    print("Exiting...")
                    exit()
            while maxTries > 0:
                userInterface.clearScreen()
                userInterface.displayLogo()
                username = input("Enter your username: \n")
                attemptedUsernames.append(username.lower())
                password = input("Enter your password: \n")
                attemptedPasswords.append(password.lower())

                if not Validation.usernameValidation(username) or not Validation.passwordValidation(password):
                    maxTries -= 1
                    print("Incorrect username or password! You have " + str(maxTries) + " attempts remaining.")
                    loggingSys.log("User tried to log into the system with invalid credentials", "False", f"username: {username}, password: {password}")
                    time.sleep(1)
                    continue

                data = dataBase.getUserData(username,password)
                if data != None:
                    print("succesfully logged in!")
                    loggedIn = True
                    user = logIn_System.loginFunc(username,password)
                    loggingSys.log("Multiple usernames and passwords are tried wrong in a row", "True")
                    time.sleep(1)
                    break
                else:
                    print("please input valid credentials")
                    time.sleep(1)
                    maxTries -= 1
        
        while loggedIn:
            userInterface.clearScreen()
            print("Logged In")
            loggingSys.log("User has succesfully logged into Unique Meal",False)
            time.sleep(1)
            userInterface.optionMenu(user,dataBase,loggingSys,backupSys)


if __name__ == '__main__':
    main()
