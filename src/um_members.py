from userInterface import UI
import os
from database import DB
from log import Logger
from checkSum import Checksum
from auth import loginAuth
import time

def main():
    def initDB():
        dbPath = os.path.join(os.path.dirname(__file__), 'uniqueMeal.db')
        dbInitialization = DB(dbPath)
        dbInitialization.create_members_table()
        dbInitialization.create_users_table()
        dbInitialization.init_superadmin()
        time.sleep(2)
    initDB()
    time.sleep(2)

    running = True
    loggedIn = False
    attemptedUsernames = []
    attemptedPasswords = []
    userInterface = UI()

    dbPath = os.path.join(os.path.dirname(__file__), 'uniqueMeal.db')
    dataBase = DB(dbPath)
    loggingSys = Logger()
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

                data = dataBase.getUserData(username,password)
                if data != None:
                    print("succesfully logged in!")
                    loggedIn = True
                    user = logIn_System.loginFunc(username,password)
                    time.sleep(2)
                    break
                else:
                    print("please input valid credentials")
                    time.sleep(2)
                    maxTries -= 1
        
        while loggedIn:
            userInterface.clearScreen()
            print("Logged In")
            userInterface.optionMenu(user,dataBase)


if __name__ == '__main__':
    main()