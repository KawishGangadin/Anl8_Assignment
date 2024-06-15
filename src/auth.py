from users import roles
from users import consultant
from users import systemAdministrator
from users import superAdministrator
from hash import hashUtils
import sqlite3

class loginAuth:
    def __init__(self,db):
        self.db = db

    def loginFunc(self, username, hashedPassword):
        username = username
        data = self.db.getUserData(username,hashedPassword)
        if data:
            dataRole = roles(data[6])
            dataID = data[0]
            if dataRole == roles.CONSULTANT:
                return consultant(dataID,username)
            elif dataRole == roles.ADMIN:
                return systemAdministrator(dataID,username)
            elif dataRole == roles.SUPERADMIN:
                return superAdministrator(dataID,username)