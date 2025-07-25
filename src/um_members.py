from userInterface import UI
import os
from database.database import DB
from log import Logger
from auth import loginAuth
from inputValidation import Validation
from backup import backup
from users import roles
from cryptoUtils import cryptoUtils
import time
import signal
import sys


def main():
    def graceful_exit(sig=None, frame=None):
        try:
            if 'loggedInUser' in locals() and loggedInUser is not None:
                loggingSys.log("User forcefully logged out (Ctrl+C)", True, username=loggedInUser.userName)
                dataBase.clearSession(loggedInUser.id,loggedInUser.session)
                print("ID: ",loggedInUser.id, " Session: ",loggedInUser.session)
        except Exception as e:
            print(f"Cleanup error: {e}")
        sys.exit(0)

    signal.signal(signal.SIGINT, graceful_exit)

    def initDB():
        dbPath = os.path.join(os.path.dirname(__file__), 'urbanMobility.db')
        dbInitialization = DB(dbPath)
        dbInitialization.createUsersTable()
        dbInitialization.initSuperadmin()
        dbInitialization.createTravellersTable()
        dbInitialization.createScootersTable()
        dbInitialization.createBackupsTable()

    initDB()
    running = True
    loggedIn = False
    attemptedUsernames = []
    attemptedPasswords = []
    userInterface = UI()

    dbPath = os.path.join(os.path.dirname(__file__), 'urbanMobility.db')
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
                attemptedPasswords.append(password)

                if not Validation.usernameValidation(username.lower()) or not Validation.passwordValidation(password):
                    maxTries -= 1
                    print("Incorrect username or password! You have " + str(maxTries) + " attempts remaining.")
                    if len(username) < 10:
                        loggingSys.log("Unsuccessful Login attempt", False, f"username: '{username}' is used for a login attempt with a wrong password")
                    else:
                        loggingSys.log("Unsuccessful Login attempt", False, "A login attempt was made with a unsupported username")

                    time.sleep(1)
                    continue
                else:
                    user = logIn_System.loginFunc(username.lower(), password)
                
                if user:
                    loggedIn = True
                    loggingSys.log("User successfully logged into Unique Meal", False, username=username.lower())
                    time.sleep(1)
                    break
                else:
                    print("Invalid username or password. Please try again.")
                    time.sleep(1)
                    maxTries -= 1
        
        while loggedIn:
            if not user:
                loggedIn = False
                break

            isTemp = dataBase.verifyAccountStatus(user.id,user.session)
            
            if isTemp != None:
                while isTemp == True:
                    print("You current password is temporary or press Q to exit the system...")
                    while True:
                        newPassword = input("Enter your new password...")

                        if newPassword.upper() == "Q":
                            print("Exiting the system")
                            exit()

                        elif Validation.passwordValidation(newPassword):
                            respone = dataBase.updatePassword(user.id,newPassword)
                            user.session += 1
                            
                            if respone == "OK":
                                loggingSys.log(f"Successfully changed {username}'s password!",False)
                                print("Password has succefully been changed")
                                loggingSys.log("User changed temporary password", False, username=username)
                                time.sleep(0.5)
                                isTemp = None
                                break

                            else:
                                loggingSys.log(f"Something went wrong trying to change {username}'s password...",False)
                                print("Something went wrong trying to change the password...")
                                loggingSys.log("User tried to change temporary password but failed", False, username=username)
                                print("Try again later! \n Exiting...")
                                exit()

                        else:
                            print("Please enter a valid password!!!")
                
                userInterface.clearScreen()
                print("Logged In")
                time.sleep(1)
                loggedInUser = user
                username, password, newPassword, user = None, None, None, None
                userInterface.optionMenu(loggedInUser,dataBase,loggingSys,backupSys)
            else:
                loggingSys.log(f"Something went wrong trying to verify {username}'s account status...",True)
                print("Something went wrong trying to verify your account's status... Try again later!!! \n Exiting...")
                exit()

if __name__ == '__main__':
    main()
