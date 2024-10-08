from locust import HttpUser, task, between
from locust.env import Environment
from locust.web import WebUI
from factory.user_factory import UserFactory
import sys

class ProductsUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def get_products(self):
        self.client.get(
            "/api/v1/products",
            headers={
                "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qbEJNa0V4UkRoRE5EZ3pSVUU1UkVVMU9UVkRSREkxTkVKQ01EYzJOa05GTmpnME5rRkdOdyJ9. (tu-token-de-autorizacion)"
            }
        )

# Parse command line arguments for the web port
web_port = 8089
if len(sys.argv) > 1:
    web_port = int(sys.argv[1].split('=')[-1])

# Create environment and runner
env = Environment(user_classes=[ProductsUser])

# Start the web UI on the specified port
web_ui = WebUI(env, host="0.0.0.0", port=web_port)
env.create_local_runner()

# Start the UI
web_ui.start()

# Run the test
env.runner.greenlet.join()