from abc import ABC, abstractmethod

class EncryptionInterface(ABC):

    @abstractmethod
    def encrypt_string(string: str) -> str:
        pass

    @abstractmethod
    def decrypt_string(string: str) -> str:
        pass