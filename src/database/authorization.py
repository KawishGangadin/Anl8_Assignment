from roles import roles


class Authorization:

    def IsAuthorized(self,userContext):
        try:
            result = self.ValidateSession(userContext.id, userContext.session, userContext.role)
            return (bool(result))
        except:
            return False

    def AuthorizeUserCreation(self, userContext, targetRole):
        try:
            if not self.IsAuthorized(userContext):
                return False
            if targetRole not in (roles.ADMIN, roles.SERVICE):
                return False

            if userContext.role == roles.SUPERADMIN:
                return targetRole in (roles.ADMIN, roles.SERVICE)

            if userContext.role == roles.ADMIN:
                return targetRole == roles.SERVICE
            return False
        except:
            return False


    def AuthorizeAction(self,userContext, requiredRole):
        try:
            if Authorization.IsAuthorized(userContext):
                return userContext.role == requiredRole
            return False
        except:
            return False

    def AuthorizeAny(self,userContext, allowedRoles):
        try:
            if not Authorization.IsAuthorized(userContext):
                return False
            return userContext.role in set(allowedRoles or [])
        except:
            return False

    def AuthorizeManage(self,userContext, targetRole):
        try:
            if not Authorization.IsAuthorized(userContext):
                return False
            if userContext.role == roles.SUPERADMIN:
                return targetRole in [roles.ADMIN, roles.SERVICE]
            if userContext.role == roles.ADMIN:
                return targetRole == roles.SERVICE
            return False

        except:
            return False

    def AuthorizeRestore(self,userContext, database, backupFileName=None, restoreCode=None):
        try:
            if not Authorization.IsAuthorized(userContext, database):
                return False
            if userContext.role == roles.SUPERADMIN:
                return True
            if userContext.role == roles.SERVICE:
                return False
            if userContext.role == roles.ADMIN:
                restoreCodePairs = database.GetRestoreCodesByUser(userContext.id)
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
