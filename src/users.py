from enum import Enum
import time
class roles(Enum):
    CONSULTANT = 'consultant'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'


class userBlueprint:
    def __init__(self, id, userName):
        self.id = id
        self.userName = userName

class consultant(userBlueprint):
    pass

class systemAdministrator(consultant):
    def displayUsers(self,db):
        allUsers = db.getUsers()
        if allUsers == None:
            print("No users found:")
        else:
            print("========List of users========")
            for user in allUsers:
                print(f"Username: {user[3]}, Role: {user[6]}\n")
        anyKey = input("Press any key to continue...")
        return
class superAdministrator(systemAdministrator):

    def testFunc(self):
        print("hello")
        time.sleep(2)