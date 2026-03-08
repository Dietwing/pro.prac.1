
from locust import HttpUser, task

class DashboardUser(HttpUser):

    @task
    def load_dashboard(self):
        self.client.get("/")
