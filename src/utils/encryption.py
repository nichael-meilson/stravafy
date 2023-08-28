import os
from cryptography.fernet import Fernet
import base64
from src.interfaces.encryption_interface import EncryptionInterface

def create_fernet() -> Fernet:
    key_string = os.environ["SECRET_KEY"].encode()
    key_bytes = base64.urlsafe_b64encode(key_string)
    return Fernet(key_bytes)

class Encryption(EncryptionInterface):
    def __init__(self) -> None:
        self.fernet: Fernet = create_fernet()

    def encrypt_string(self, string: str) -> str:
        return str(self.fernet.encrypt(string.encode()))
    
    def decrypt_string(self, string: str) -> str:
        return str(self.fernet.decrypt(string.encode()))

