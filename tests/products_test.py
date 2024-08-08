from locust import HttpUser, task, between
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
from prometheus_client import start_http_server, Summary
import gevent
from factory.user_factory import UserFactory

# Configuración de logging
setup_logging("INFO", None)

# Definir la métrica para rastrear la duración de las funciones
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class ProductsUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def perform_task(self):
        with REQUEST_TIME.time():  # Rastrea el tiempo de la solicitud
            self.client.get(
                "/api/v1/products",
                headers={
                    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qbEJNa0V4UkRoRE5EZ3pSVUU1UkVVMU9UVkRSREkxTkVKQ01EYzJOa05GTmpnME5rRkdOdyJ9.eyJpc3MiOiJodHRwczovL2Rldi0zaXBmNXFtMi5hdXRoMC5jb20vIiwic3ViIjoid1VnaFdDaWdFY1NNMXBza25TdzNac0RDOTd0Z2RoWGxAY2xpZW50cyIsImF1ZCI6ImN5cHJlc3MiLCJpYXQiOjE3MjE1ODQ4NTEsImV4cCI6MTcyMTY3MTI1MSwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoid1VnaFdDaWdFY1NNMXBza25TdzNac0RDOTd0Z2RoWGwiLCJwZXJtaXNzaW9ucyIsW119.igKq4f4jLZaZiYGzpzFPM6urgxgeYcqAni0AK_hfB4gvodWLrL6irdN22DfCaNak4c85qFVjAvMzCPgP3YAtPF0C0dJS6onvzQcBSlsG_ELZeQG74k7RaOk8gfvOZqA4KaULo12Z19ppWkv_-s6QtLBKGLQXFI09zeKp8EAoV48_m_biAXL8kHjzTA8DHr-4Ms5N4BxNmVRwBrxw9CCnuvVhdK9_vyM_xB4KDnuVQw8ywZHk2rpfZ30aTHJLLjUFWBikpSwi1lEHjlw5zA0SHtvkkHp_Y2CPK04E6tu2cPYvtBcYsi8r2XoddGeirgrJpL4LlUra8EZRlgfFz4onYA"
                }
            )

# Crear environment y runner
UserClass = UserFactory.create_user("products")
env = Environment(user_classes=[UserClass])
env.create_local_runner()

# Función para rastrear la duración de las solicitudes
@REQUEST_TIME.time()
def perform_task():
    # Aquí llamas al método de la clase del usuario que realiza la solicitud
    user_instance = UserClass(env)
    user_instance.perform_task()

# Iniciar un greenlet que periódicamente muestra las estadísticas actuales
gevent.spawn(stats_printer(env.stats))
gevent.spawn(stats_history, env.runner)

# Iniciar el exportador de Prometheus en el puerto 8000
start_http_server(8000)

# Iniciar la prueba
env.runner.start(10, spawn_rate=2)  # 10 usuarios, tasa de generación de 2 usuarios por segundo

# Detener la prueba después de 1 minuto
gevent.spawn_later(60, lambda: env.runner.quit())

# Esperar a que los greenlets terminen
env.runner.greenlet.join()
