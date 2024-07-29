from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2.5)  # Tiempo de espera entre tareas en segundos

    @task
    def my_task(self):
        self.client.get("/")  # Realiza una solicitud GET a la raíz del servidor
        self.client.post("/submit", {"key": "value"})  # Realiza una solicitud POST con algunos datos
