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
    
    def updateSession(self, db,loggingSys):
        try:
            result = db.updateSession(self.id,self.session)
            if result:
                self.session = result
        except Exception as e:
            pass