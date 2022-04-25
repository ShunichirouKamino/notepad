from locust import HttpUser, between, task


class QuickStartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def hello(self):
        self.client.get("/sandbox/greet")