import os
from cryptography.fernet import Fernet
from interfaces.encryption_interface import EncryptionInterface

class Encryption(EncryptionInterface):
    def __init__(self) -> None:
        self.fernet: Fernet = Fernet(os.environ["SECRET_KEY"].encode())

    def encrypt_string(self, string: str) -> str:
        return str(self.fernet.encrypt(string.encode()))
    
    def decrypt_string(self, string: str) -> str:
        return str(self.fernet.decrypt(string.encode()))

