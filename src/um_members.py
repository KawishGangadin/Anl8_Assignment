from userInterface import UI
from database import DB
from log import Logger
import time

def main():
    def initDB():
        dbInitialization = DB('src/uniqueMeal.db')
        dbInitialization.create_members_table()
        dbInitialization.create_users_table()
        dbInitialization.init_superadmin()
        print("tables created")
    initDB()

    running = True
    loggedIn = False
    userInterface = UI()

    dataBase = DB('src/uniqueMeal.db')
    loggingSys = Logger()
    while running:
        maxTries = 3
        while not loggedIn:
            while maxTries > 0:
                userInterface.clearScreen()
                userInterface.displayLogo()
                username = input("Enter your username: \n")
                password = input("Enter your password: \n")
                loggedIn = True
                break
        while loggedIn:
            userInterface.clearScreen()
            print("Logged In")

if __name__ == '__main__':
    main()