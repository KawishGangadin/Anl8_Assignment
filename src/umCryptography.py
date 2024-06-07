from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

class encryption:

    @staticmethod
    def get_private_key():
        # get encryption password from environment variable
        password = os.environ.get('PRIVATE_KEY_PASSWORD')
        if not password:
            # If the password is not set, prompt the user to input it
            print("Private key password not found. Please set the PRIVATE_KEY_PASSWORD environment variable.")
            password = input("Enter the private key password: ")
            if not password:
                raise ValueError("Private key password not provided.")
        try:
            with open('private_key.pem', 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=password.encode()
                )
                return private_key
        except FileNotFoundError:
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            with open('private_key.pem', 'wb') as f:
                private_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
                )
                f.write(private_pem)
            return private_key


    @staticmethod
    def get_public_key():
        public_key = encryption.get_private_key().public_key()
        return public_key

    @staticmethod
    def decrypt_data(encrypted_data):
        decrypted = encryption.get_private_key().decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

    @staticmethod
    def encrypt_data(data):
        encrypted = encryption.get_public_key().encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted
