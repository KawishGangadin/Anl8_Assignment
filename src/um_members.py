from userInterface import UI
import os
from database import DB
from log import Logger
from auth import loginAuth
from inputValidation import Validation
from backup import backup
from users import roles
from cryptoUtils import cryptoUtils
import time

def main():
    def initDB():
        dbPath = os.path.join(os.path.dirname(__file__), 'uniqueMeal.db')
        dbInitialization = DB(dbPath)
        dbInitialization.createMembersTable()
        dbInitialization.createUsersTable()
        dbInitialization.initSuperadmin()
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
                    loggingSys.log("Unsuccesful login attempt", True, "Multiple usernames and passwords are tried wrong in a row")
                    print("Exiting...")
                    exit()

                else:
                    print("A user tried to log into the system too many times with the wrong credentials")
                    loggingSys.log("Unsuccesful login attempt", True,"A user tried to log into the system too many times with the wrong credentials")
                    print("Exiting...")
                    exit()

            while maxTries > 0:
                userInterface.clearScreen()
                userInterface.displayLogo()
                username = input("Enter your username: \n")
                attemptedUsernames.append(username.lower())
                password = input("Enter your password: \n")
                attemptedPasswords.append(password.lower())

                if not Validation.usernameValidation(username.lower(), username, loggingSys) or not Validation.passwordValidation(password, username, loggingSys):
                    maxTries -= 1
                    print("Incorrect username or password! You have " + str(maxTries) + " attempts remaining.")
                    loggingSys.log("Unsuccesful Login attempt", "False", f"username: '{username}' is used for a login attempt with a wrong password")
                    time.sleep(1)
                    continue
                data = dataBase.getUserData(username.lower())
                
                if data:
                    storedPassword = data[4]
                    storedSalt = data[8] 

                    if cryptoUtils.verifyPassword(password, storedPassword, storedSalt):
                        print("Successfully logged in!")
                        loggedIn = True
                        user = logIn_System.loginFunc(username.lower(), password)
                        loggingSys.log("User successfully logged into Unique Meal", False, username=username.lower())
                        time.sleep(1)
                        break

                    else:
                        print("Invalid username or password. Please try again.")
                        time.sleep(1)
                        maxTries -= 1

                else:
                    print("Invalid username or password. Please try again.")
                    time.sleep(1)
                    maxTries -= 1
        
        while loggedIn:
            # make sure to go back to login screen if user logs out
            if not data:
                loggedIn = False
                break

            isTemp = data[7]

            while isTemp == True:
                print("You current password is temporary or press Q to exit the system...")
                while True:
                    newPassword = input("Enter your new password...")

                    if newPassword.upper() == "Q":
                        print("Exiting the system")
                        exit()

                    elif Validation.passwordValidation(newPassword, username, loggingSys):
                        respone = dataBase.updatePassword(user.id,newPassword)
                        
                        if respone == "OK":
                            loggingSys.log(f"Successfully changed {username}'s password!",False)
                            print("Password has succefully been changed")
                            time.sleep(0.5)
                            isTemp = None
                            break

                        else:
                            loggingSys.log(f"Something went wrong trying to change {username}'s password...",False)
                            print("Something went wrong trying to change the password...")
                            print("Try again later! \n Exiting...")
                            exit()

                    else:
                        print("Please enter a valid password!!!")
                        
            userInterface.clearScreen()
            print("Logged In")
            time.sleep(1)
            username, password, newPassword, data = None, None, None, None
            userInterface.optionMenu(user,dataBase,loggingSys,backupSys)

if __name__ == '__main__':
    main()
