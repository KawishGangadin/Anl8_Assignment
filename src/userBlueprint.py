class userBlueprint:
    def __init__(self, id, role, userName, db, session):
        self._id = id
        self._userName = userName
        self._db = db
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

    @property
    def db(self):
        return self._db