class userBlueprint:
    def __init__(self, id, userName,db,session):
        self.id = id
        self.userName = userName
        self.db = db 
        self.session = session