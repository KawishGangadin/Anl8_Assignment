from roles import roles


class Authorization:

    @staticmethod
    def IsAuthorized(userContext, database):
        try:
            result = database.validateSession(userContext.id, userContext.session, userContext.role)
            return bool(result)
        except:
            return False

    @staticmethod
    def AuthorizeAction(userContext, requiredRole, database):
        try:
            if Authorization.IsAuthorized(userContext, database):
                return userContext.role == requiredRole
            return False
        except:
            return False

    @staticmethod
    def AuthorizeAny(userContext, allowedRoles, database):
        try:
            if not Authorization.IsAuthorized(userContext, database):
                return False
            return userContext.role in set(allowedRoles or [])
        except:
            return False

    @staticmethod
    def AuthorizeManage(userContext, targetRole, database):
        try:
            if not Authorization.IsAuthorized(userContext, database):
                return False
            if userContext.role == roles.SUPER_ADMIN:
                return targetRole in [roles.ADMIN, roles.SERVICE]
            if userContext.role == roles.ADMIN:
                return targetRole == roles.SERVICE
            return False

        except:
            return False

    @staticmethod
    def AuthorizeRestore(userContext, database, backupFileName=None, restoreCode=None):
        try:
            if not Authorization.IsAuthorized(userContext, database):
                return False
            if userContext.role == roles.SUPER_ADMIN:
                return True
            if userContext.role == roles.SERVICE:
                return False
            if userContext.role == roles.ADMIN:
                restoreCodePairs = database.getRestoreCodesByUser(userContext.id)
                if not restoreCodePairs:
                    return False

                for storedCode, storedFileName in restoreCodePairs:
                    if storedCode == restoreCode and storedFileName == backupFileName:
                        if hasattr(database, "isRestoreCodeUsed") and database.isRestoreCodeUsed(userContext.id, storedCode):
                            return False
                        return True

                return False

            return False

        except:
            return False
