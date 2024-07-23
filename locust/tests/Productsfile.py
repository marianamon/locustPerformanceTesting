from locust import HttpUser, task, between, events
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent

setup_logging("INFO", None)

class UserBehavior(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def get_products(self):
        self.client.get(
            "/api/v1/products",
            headers={
                "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qbEJNa0V4UkRoRE5EZ3pSVUU1UkVVMU9UVkRSREkxTkVKQ01EYzJOa05GTmpnME5rRkdOdyJ9.eyJpc3MiOiJodHRwczovL2Rldi0zaXBmNXFtMi5hdXRoMC5jb20vIiwic3ViIjoid1VnaFdDaWdFY1NNMXBza25TdzNac0RDOTd0Z2RoWGxAY2xpZW50cyIsImF1ZCI6ImN5cHJlc3MiLCJpYXQiOjE3MjE1ODQ4NTEsImV4cCI6MTcyMTY3MTI1MSwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoid1VnaFdDaWdFY1NNMXBza25TdzNac0RDOTd0Z2RoWGwiLCJwZXJtaXNzaW9ucyI6W119.igKq4f4jLZaZiYGzpzFPM6urgxgeYcqAni0AK_hfB4gvodWLrL6irdN22DfCaNak4c85qFVjAvMzCPgP3YAtPF0C0dJS6onvzQcBSlsG_ELZeQG74k7RaOk8gfvOZqA4KaULo12Z19ppWkv_-s6QtLBKGLQXFI09zeKp8EAoV48_m_biAXL8kHjzTA8DHr-4Ms5N4BxNmVRwBrxw9CCnuvVhdK9_vyM_xB4KDnuVQw8ywZHk2rpfZ30aTHJLLjUFWBikpSwi1lEHjlw5zA0SHtvkkHp_Y2CPK04E6tu2cPYvtBcYsi8r2XoddGeirgrJpL4LlUra8EZRlgfFz4onYA"
            }
        )

# Create environment and runner
env = Environment(user_classes=[UserBehavior])
env.create_local_runner()

# Start a greenlet that periodically outputs the current stats
gevent.spawn(stats_printer(env.stats))
gevent.spawn(stats_history, env.runner)

# Start the test
env.runner.start(10, spawn_rate=2)  # 10 users, spawn rate 2 users per second

# Stop the test after 1 minute
gevent.spawn_later(60, lambda: env.runner.quit())

# Wait for the greenlets
env.runner.greenlet.join()
