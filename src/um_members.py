from userInterface import UI
import os
from database.database import DB
from log import Logger
from authentication import LoginAuthentication
from inputValidation import InputValidation
from backup import Backup
import time
import signal
from utility import Utility
import sys

def main():
    def GracefulExit(sig=None, frame=None):
        try:
            if 'loggedInUser' in locals() and loggedInUser is not None:
                loggingSys.Log("User forcefully logged out (Ctrl+C)", True, username=loggedInUser.userName)
                dataBase.ClearSession(loggedInUser.id,loggedInUser.session)
                print("ID: ",loggedInUser.id, " Session: ",loggedInUser.session)
        except Exception as e:
            print(f"Cleanup error: {e}")
        sys.exit(0)

    signal.signal(signal.SIGINT, GracefulExit)

    def InitalizeDatabase():
        dbPath = os.path.join(os.path.dirname(__file__), 'urbanMobility.db')
        dbInitialization = DB(dbPath)
        dbInitialization.CreateUsersTable()
        dbInitialization.InitSuperadmin()
        dbInitialization.CreateTravellersTable()
        dbInitialization.CreateScootersTable()
        dbInitialization.CreateBackupsTable()

    InitalizeDatabase()
    running = True
    loggedIn = False
    attemptedUsernames = []
    attemptedPasswords = []
    userInterface = UI()

    dbPath = os.path.join(os.path.dirname(__file__), 'urbanMobility.db')
    dataBase = DB(dbPath)
    loggingSys = Logger()
    backupSys = Backup()
    logIn_System = LoginAuthentication(dataBase)

    while running:
        maxTries = 3
        while not loggedIn:
            if maxTries <= 0:
                if len(set(attemptedPasswords)) > 1 and len(set(attemptedUsernames)) > 1:
                    print("Multiple usernames and passwords are tried wrong in a row")
                    loggingSys.Log("Unsuccesful login attempt", True, "Multiple usernames and passwords are tried wrong in a row")
                    print("Exiting...")
                    exit()
                else:
                    print("A user tried to log into the system too many times with the wrong credentials")
                    loggingSys.Log("Unsuccesful login attempt", True,"A user tried to log into the system too many times with the wrong credentials")
                    print("Exiting...")
                    exit()

            while maxTries > 0:
                userInterface.ClearScreen()
                userInterface.DisplayLogo()
                username = input("Enter your username: \n")
                attemptedUsernames.append(username.lower())
                password = input("Enter your password: \n")
                attemptedPasswords.append(password)

                if not InputValidation.ValidateUsername(username.lower()) or not InputValidation.ValidatePassword(password):
                    maxTries -= 1
                    print("Incorrect username or password! You have " + str(maxTries) + " attempts remaining.")
                    if len(username) < 10:
                        loggingSys.Log("Unsuccessful Login attempt", False, f"username: '{username}' is used for a login attempt with a wrong password")
                    else:
                        loggingSys.Log("Unsuccessful Login attempt", False, "A login attempt was made with a unsupported username")

                    time.sleep(1)
                    continue
                else:
                    user = logIn_System.Login(username.lower(), password)
                
                if user:
                    loggedIn = True
                    loggingSys.Log("User successfully logged into Unique Meal", False, username=username.lower())
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

            isTemp = dataBase.VerifyAccountStatus(user.id,user.session)
            
            if isTemp != None:
                while isTemp == True:
                    print("You current password is temporary or press Q to exit the system...")
                    while True:
                        newPassword = input("Enter your new password...")

                        if newPassword.upper() == "Q":
                            dataBase.ClearSession(user.id, user.session)
                            print("Exiting the system")

                            exit()

                        elif InputValidation.ValidatePassword(newPassword):
                            respone = dataBase.UpdateOwnPassword(user.id,newPassword,user.GetUserContext())
                            user.UpdateSession(dataBase,loggingSys)
                            
                            if respone == "OK":
                                loggingSys.Log(f"Successfully changed {username}'s password!",False)
                                print("Password has succefully been changed")
                                loggingSys.Log("User changed temporary password", False, username=username)
                                time.sleep(0.5)
                                isTemp = None
                                break

                            else:
                                loggingSys.Log(f"Something went wrong trying to change {username}'s password...",False)
                                print("Something went wrong trying to change the password...")
                                loggingSys.Log("User tried to change temporary password but failed", False, username=username)
                                print("Try again later! \n Exiting...")
                                exit()

                        else:
                            print("Please enter a valid password!!!")
                
                userInterface.ClearScreen()
                print("Logged In")
                time.sleep(1)
                loggedInUser = user
                username, password, newPassword, user = None, None, None, None
                userInterface.OptionMenu(loggedInUser,dataBase,loggingSys,backupSys)
            else:
                loggingSys.Log(f"Something went wrong trying to verify {username}'s account status...",True)
                print("Something went wrong trying to verify your account's status... Try again later!!! \n Exiting...")
                exit()

if __name__ == '__main__':
    main()

