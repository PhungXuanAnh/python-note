import time
from locust import HttpUser, task, between

"""
    NOTE: Meaning of terms after analysis in Locust Load Testing
    see here: https://stackoverflow.com/a/53145593/7639845
"""

endpoint = '/todo/api/v1.0/servers'
weight = 3

class QuickstartUser(HttpUser):
    """
        This class will test api from this code: python-note/flask_sample/simple_apis/flask_simple.py
    """
    
    wait_time = between(1, 2)           # simulated user will wait 1 to 2 second each task

        
    @task
    def get_a(self):
        self.client.get(endpoint + '/1')

    # @task(3)    # weight=3 mean this task will be call 3 time each 1 time call get_a() task
    # def get_all(self):
    #     self.client.get(endpoint)

    def on_start(self):
        # start for each simulated user
        # don't do anything on start, maybe create initial data
        pass

    def on_stop(self):
        pass
