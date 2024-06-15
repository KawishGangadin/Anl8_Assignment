from users import roles
from users import consultant
from users import systemAdministrator
from users import superAdministrator
import sqlite3

class loginAuth:
    def __init__(self,db):
        self.db = db

    def loginFunc(self, username, password):
        username = username
        password = password
        data = self.db.getUserData(username,password)
        if data:
            dataRole = roles(data[6])
            dataID = data[0]
            if dataRole == roles.CONSULTANT:
                return consultant(dataID,username)
            elif dataRole == roles.ADMIN:
                return systemAdministrator(dataID,username)
            elif dataRole == roles.SUPERADMIN:
                return superAdministrator(dataID,username)