from users import roles
from users import service
from users import systemAdministrator
from users import superAdministrator
from cryptoUtils import cryptoUtils

class loginAuth:
    def __init__(self, db):
        self.db = db

    def loginFunc(self, username, password):
        try:
            user = self.db.verifyUserLogin(username,password)

            roleType = user["role"]
            print(roleType)
            print(roles.SUPERADMIN)
            if roleType == roles.SERVICE.value:
                return service(user["id"], roles.SERVICE, user["username"], user["sessionID"])
            elif roleType == roles.ADMIN.value:
                return systemAdministrator(user["id"], roles.ADMIN, user["username"],  user["sessionID"])
            elif roleType == roles.SUPERADMIN.value:
                return superAdministrator(user["id"], roles.SUPERADMIN, user["username"], user["sessionID"])
            else:
                print("Unknown role detected")
                return None
        except Exception as e:
            print("User not found.")
            return None