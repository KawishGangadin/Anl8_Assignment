from users import roles
from users import service
from users import systemAdministrator
from users import superAdministrator
from cryptoUtils import cryptoUtils

class loginAuth:
    def __init__(self, db):
        self.db = db

    def loginFunc(self, username, password):
        """Logging in with a user

        In deze functie kan de user worden ingelogd,
        deze wordt aangeroepen binnen de main file nadat de user 
        een username en een password heeft ingevoerd.
        Is het correct? Een class wordt gereturned van die specifieke user type
        """
        try:
            user = self.db.verifyUserLogin(username,password)

            roleType = user["role"]
            print(roleType)
            print(roles.SUPERADMIN)
            if roleType == roles.SERVICE.value:
                return service(user["id"], roles.SERVICE, user["username"], self.db, user["sessionID"])
            elif roleType == roles.ADMIN.value:
                return systemAdministrator(user["id"], roles.ADMIN, user["username"], self.db, user["sessionID"])
            elif roleType == roles.SUPERADMIN.value:
                return superAdministrator(user["id"], roles.SUPERADMIN, user["username"], self.db, user["sessionID"])
            else:
                print("Unknown role detected")
                return None
        except Exception as e:
            print("User not found.")
            return None