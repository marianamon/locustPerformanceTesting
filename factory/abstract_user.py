from locust import HttpUser, task, between
from abc import ABC, abstractmethod

class AbstractUser(HttpUser, ABC):
    wait_time = between(1, 2.5)

    @abstractmethod
    @task
    def perform_task(self):
        pass
