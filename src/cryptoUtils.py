import os
import hashlib
import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

class cryptoUtils:
    keys_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys')

    @staticmethod
    def generateKeyPair(keySize=2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=keySize,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def serializePrivateKey(private_key, password=None):
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
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    @staticmethod
    def saveKeys():
        os.makedirs(cryptoUtils.keys_folder, exist_ok=True)

        private_key, public_key = cryptoUtils.generateKeyPair()

        private_key_pem = cryptoUtils.serializePrivateKey(private_key)
        private_key_file = os.path.join(cryptoUtils.keys_folder, 'private.pem')
        with open(private_key_file, 'wb') as f:
            f.write(private_key_pem)

        public_key_pem = cryptoUtils.serializePublicKey(public_key)
        public_key_file = os.path.join(cryptoUtils.keys_folder, 'public.pem')
        with open(public_key_file, 'wb') as f:
            f.write(public_key_pem)

        print(f"Keys saved successfully in the '{cryptoUtils.keys_folder}' folder.")

    @staticmethod
    def loadPrivateKey():
        private_key_file = os.path.join(cryptoUtils.keys_folder, 'private.pem')
        with open(private_key_file, 'rb') as f:
            pem_data = f.read()
            private_key = serialization.load_pem_private_key(
                pem_data,
                password=None,
                backend=default_backend()
            )
        return private_key

    @staticmethod
    def loadPublicKey():
        public_key_file = os.path.join(cryptoUtils.keys_folder, 'public.pem')
        with open(public_key_file, 'rb') as f:
            pem_data = f.read()
            public_key = serialization.load_pem_public_key(
                pem_data,
                backend=default_backend()
            )
        return public_key

    @staticmethod
    def encryptWithPublicKey(public_key, message):
        ciphertext = public_key.encrypt(
            message.encode('utf-8'), 
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    @staticmethod
    def decryptWithPrivateKey(private_key, ciphertext):
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
        salt = secrets.token_bytes(32)
        hashedPassword = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return hashedPassword, salt

    @staticmethod
    def verifyPassword(providedPassword, storedPassword, salt):
        hashedProvidedPassword = hashlib.pbkdf2_hmac(
            'sha256',
            providedPassword.encode('utf-8'),
            salt,
            100000
        )
        return hashedProvidedPassword == storedPassword
    