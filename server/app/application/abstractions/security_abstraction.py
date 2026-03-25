from abc import ABC, abstractmethod
from typing import Dict, Any


class ISecurityService(ABC):
    @abstractmethod
    def hash_password(self, plain_password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def create_access_token(self, payload: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_refresh_token(self, payload: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def decode_refresh_token(self, token: str) -> Dict[str, Any]:
        pass