import os
import hashlib
import secrets

class cryptoUtils:

    @staticmethod
    def generateKeyPair(keySize=2048):
        # Generate RSA key pair
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import serialization
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=keySize,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def serializePrivateKey(private_key, password=None):
        # Serialize private key to PEM format
        from cryptography.hazmat.primitives import serialization
        encryption_algorithm = (
            serialization.BestAvailableEncryption(password)
            if password else
            serialization.NoEncryption()
        )
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )
        return pem

    @staticmethod
    def serializePublicKey(public_key):
        # Serialize public key to PEM format
        from cryptography.hazmat.primitives import serialization
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    @staticmethod
    def loadPrivateKey(pem, password=None):
        # Load private key from PEM format
        from cryptography.hazmat.primitives import serialization
        private_key = serialization.load_pem_private_key(
            pem,
            password=password,
            backend=default_backend()
        )
        return private_key

    @staticmethod
    def loadPublicKey(pem):
        # Load public key from PEM format
        from cryptography.hazmat.primitives import serialization
        public_key = serialization.load_pem_public_key(
            pem,
            backend=default_backend()
        )
        return public_key

    @staticmethod
    def encryptWithPublicKey(public_key, message):
        # Encrypt message with RSA-OAEP using public key
        from cryptography.hazmat.primitives.asymmetric import padding
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    @staticmethod
    def decryptWithPrivateKey(private_key, ciphertext):
        # Decrypt ciphertext with RSA-OAEP using private key
        from cryptography.hazmat.primitives.asymmetric import padding
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    @staticmethod
    def hashPassword(password):
        # Hash password using PBKDF2 with SHA-256 and a random salt
        salt = secrets.token_bytes(32)  # Generate a random salt
        hashedPassword = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return hashedPassword, salt

    @staticmethod
    def verifyPassword(providedPassword, storedPassword, salt):
        # Verify provided password against stored password using salt
        hashedProvidedPassword = hashlib.pbkdf2_hmac(
            'sha256',
            providedPassword.encode('utf-8'),
            salt,
            100000
        )
        return hashedProvidedPassword == storedPassword
