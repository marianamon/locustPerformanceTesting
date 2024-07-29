from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
from prometheus_client import start_http_server
import gevent
from factory.user_factory import UserFactory

setup_logging("INFO", None)

# Create environment and runner
UserClass = UserFactory.create_user("products")
env = Environment(user_classes=[UserClass])
env.create_local_runner()

# Start a greenlet that periodically outputs the current stats
gevent.spawn(stats_printer(env.stats))
gevent.spawn(stats_history, env.runner)

# Start the Prometheus exporter on port 8000
start_http_server(8000)

# Start the test
env.runner.start(10, spawn_rate=2)  # 10 users, spawn rate 2 users per second

# Stop the test after 1 minute
gevent.spawn_later(60, lambda: env.runner.quit())

# Wait for the greenlets
env.runner.greenlet.join()
