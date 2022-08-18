# Print "locust" into the Bash to start load test
from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        self.client.get('/')

    @task
    def string_req(self):
        self.client.get('/string/', { "data": "test_string"})

    @task
    def ndarray_req(self):
        self.client.get('/ndarray/', { "data" : [0, 1] })    