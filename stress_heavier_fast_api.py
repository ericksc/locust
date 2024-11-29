"""
locust Stress test
"""
import socket
import json
import gevent

from locust import HttpUser, task, between
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging

setup_logging("INFO", None)

class User(HttpUser):
    """
    user class def
    """
    timeout_sec = 10
    wait_time = between(0, timeout_sec)

    # local host address
    host = "http://127.0.0.1:8002"

    @task
    def my_task(self):
        """

        :return:
        """
        # based on endpoint request body
        entry_data = {
            "get_id": "string",
            "type": "string",
            "name": "string",
            "antsRequired": 0,
            "timeRequired": 0
        }

        self.client.get(
            url=f"/",
            headers={
                     "Accept": "application/json",
                     "Content-Type": "application/json",
                     })

env = Environment(user_classes=[User])
env.create_local_runner()

# setup Environment and Runner

# start a WebUI instance
env.create_web_ui("127.0.0.1", 8089)

# periodically outputs the current stats
gevent.spawn(stats_printer(env.stats))
gevent.spawn(stats_history, env.runner)

# start the test
NUSER =4

USER_INCREASE_PER_SECOND = 20
env.runner.start(NUSER, spawn_rate=USER_INCREASE_PER_SECOND)

# in 60 seconds stop the runner
RUN_DURATION_SECONDS = 60
gevent.spawn_later(RUN_DURATION_SECONDS, lambda: env.runner.quit()) # pylint: disable=unnecessary-lambda

# wait for the greenlets
env.runner.greenlet.join()

# stop the web server for good measures
env.web_ui.stop()
