from roles import roles

class UserContext:
    def __init__(self, id, role, session):
        self.id = id
        self.role = role
        self.session = session


class userBlueprint:
    def __init__(self, id, role, userName, session):
        self._id = id
        self._userName = userName
        self._role = role
        self.session = session

    @property
    def id(self):
        return self._id

    @property
    def role(self):
        return self._role

    @property
    def userName(self):
        return self._userName

    def GetUserContext(self):
        return UserContext(self.id, self.role, self.session)

    def updateSession(self, db, loggingSys):
        try:
            result = db.updateSession(self.id, self.session)
            if result:
                self.session = result
        except Exception as e:
            if loggingSys:
                loggingSys.log(f"Session update failed: {e}", True, username=self.userName)
