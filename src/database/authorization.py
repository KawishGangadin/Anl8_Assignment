from roles import roles


class Authorization:

    def IsAuthorized(self,userContext):
        try:
            result = self.ValidateSession(userContext.id, userContext.session, userContext.role)
            return (bool(result))
        except:
            return False

    def AuthorizeUserManagement(self, userContext, targetRole):
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

    def AuthorizeTavellerManagement(self, userContext):
        try:
            if not self.IsAuthorized(userContext):
                return False

            return userContext.role in (roles.SUPERADMIN, roles.ADMIN)
        except:
            return False

    def AuthorizeAction(self,userContext, requiredRole):
        try:
            if self.IsAuthorized(userContext):
                return userContext.role == requiredRole
            return False
        except:
            return False

    def AuthorizeAny(self,userContext, allowedRoles):
        try:
            if not self.IsAuthorized(userContext):
                return False
            print(userContext.role)
            print(allowedRoles)
            return userContext.role in allowedRoles
        except:
            return False
