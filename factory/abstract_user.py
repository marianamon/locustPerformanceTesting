from locust import HttpUser
from abc import ABC, abstractmethod

class BaseUserMeta(type(HttpUser), type(ABC)):
    pass

class AbstractUser(HttpUser, ABC, metaclass=BaseUserMeta):
    @abstractmethod
    def some_method(self):
        pass
