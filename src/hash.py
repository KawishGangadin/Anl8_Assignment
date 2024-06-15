import hashlib

class hashUtils:
    @staticmethod
    def hashPassword(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def compareHashes(hashed1, hashed2):
        return hashed1 == hashed2