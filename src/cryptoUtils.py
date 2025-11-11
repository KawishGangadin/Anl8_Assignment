import os
import hashlib
import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

class CryptoUtils:
    keysFolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys')

    @staticmethod
    def GenerateKeyPair(sizeOfKey=2048):
        privateKey = rsa.generate_private_key(
            public_exponent=65537,
            keySize=sizeOfKey,
            backend=default_backend()
        )
        publicKey = privateKey.public_key()
        return privateKey, publicKey

    @staticmethod
    def SerializePrivateKey(privateKey, password=None):
        encryption_algorithm = (
            serialization.BestAvailableEncryption(password)
            if password else
            serialization.NoEncryption()
        )
        pem = privateKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm
        )
        return pem

    @staticmethod
    def SerializePublicKey(publicKey):
        pem = publicKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    @staticmethod
    def SaveKeys():
        os.makedirs(CryptoUtils.keysFolder, exist_ok=True)

        privateKey, public_key = CryptoUtils.GenerateKeyPair()

        privateKeyPEM = CryptoUtils.SerializePrivateKey(privateKey)
        privateKeyFile = os.path.join(CryptoUtils.keysFolder, 'private.pem')
        with open(privateKeyFile, 'wb') as f:
            f.write(privateKeyPEM)

        publicKeyPEM = CryptoUtils.SerializePublicKey(public_key)
        publicKeyFile = os.path.join(CryptoUtils.keysFolder, 'public.pem')
        with open(publicKeyFile, 'wb') as f:
            f.write(publicKeyPEM)

        print(f"Keys saved successfully in the '{CryptoUtils.keysFolder}' folder.")

    @staticmethod
    def LoadPrivateKey():
        privateKey = os.path.join(CryptoUtils.keysFolder, 'private.pem')
        with open(privateKey, 'rb') as f:
            pemData = f.read()
            private_key = serialization.load_pem_private_key(
                pemData,
                password=None,
                backend=default_backend()
            )
        return private_key

    @staticmethod
    def LoadPublicKey():
        publicKeyFile = os.path.join(CryptoUtils.keysFolder, 'public.pem')
        with open(publicKeyFile, 'rb') as f:
            pemData = f.read()
            publicKey = serialization.load_pem_public_key(
                pemData,
                backend=default_backend()
            )
        return publicKey

    @staticmethod
    def EncryptWithPublicKey(publicKey, message):
        maxChunkSize = 190

        message_bytes = message.encode('utf-8')
        ciphertext_chunks = []

        for i in range(0, len(message_bytes), maxChunkSize):
            chunk = message_bytes[i:i+maxChunkSize]
            encryptedChunk = publicKey.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            ciphertext_chunks.append(encryptedChunk)

        return b"".join(ciphertext_chunks)


    @staticmethod
    def DecryptWithPrivateKey(privateKey, ciphertext):
        keySizeInBytes = privateKey.key_size // 8
        plaintextChunks = []

        for i in range(0, len(ciphertext), keySizeInBytes):
            chunk = ciphertext[i:i+keySizeInBytes]
            decryptedChunk = privateKey.decrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            plaintextChunks.append(decryptedChunk)
        return b"".join(plaintextChunks).decode('utf-8')

    @staticmethod
    def HashPassword(password):
        salt = secrets.token_bytes(32)
        hashedPassword = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return hashedPassword, salt

    @staticmethod
    def VerifyPassword(providedPassword, storedPassword, salt):
        hashedProvidedPassword = hashlib.pbkdf2_hmac(
            'sha256',
            providedPassword.encode('utf-8'),
            salt,
            100000
        )
        return hashedProvidedPassword == storedPassword
    