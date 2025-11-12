from users import roles
from users import Service
from users import SystemAdministrator
from users import SuperAdministrator

class LoginAuthentication:
    def __init__(self, db):
        self.db = db

    def Login(self, username, password):
        try:
            user = self.db.VerifyUserLogin(username,password)

            roleType = user["role"]
            print(roleType)
            print(roles.SUPERADMIN)
            if roleType == roles.SERVICE.value:
                return Service(user["id"], roles.SERVICE, user["username"], user["sessionID"])
            elif roleType == roles.ADMIN.value:
                return SystemAdministrator(user["id"], roles.ADMIN, user["username"],  user["sessionID"])
            elif roleType == roles.SUPERADMIN.value:
                return SuperAdministrator(user["id"], roles.SUPERADMIN, user["username"], user["sessionID"])
            else:
                print("Unknown role detected")
                return None
        except Exception as e:
            print("User not found.")
            return None