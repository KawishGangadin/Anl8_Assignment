from enum import Enum
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
    pass

class superAdministrator(systemAdministrator):
    pass