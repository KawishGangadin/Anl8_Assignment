class Authorization:
    @staticmethod
    def validatePrivileges(user, intendedRole, db, logger=None):
        if user is None:
            if logger:
                logger.log("Authorization failed: user is None", True)
            return False

        try:
            sessionValid = db.validateSession(user.id, user.session)
        except Exception as e:
            if logger:
                logger.log(f"Authorization failed: session validation error ({e})", True, username=getattr(user, "userName", None))
            return False

        if not sessionValid:
            if logger:
                logger.log("Authorization failed: invalid or expired session", True, username=getattr(user, "userName", None))
            return False

        userRole = getattr(user, "role", None)
        if hasattr(userRole, "name"):
            userRole = userRole.name
        elif hasattr(userRole, "value"):
            userRole = userRole.value

        intendedRoleValue = getattr(intendedRole, "name", None) or getattr(intendedRole, "value", None) or str(intendedRole)

        if str(userRole).upper() != str(intendedRoleValue).upper():
            if logger:
                logger.log(f"Authorization failed: insufficient role (have: {userRole}, need: {intendedRoleValue})", True, username=getattr(user, "userName", None))
            return False

        if logger:
            logger.log(f"Authorization success for role {intendedRoleValue}", False, username=getattr(user, "userName", None))
        return True