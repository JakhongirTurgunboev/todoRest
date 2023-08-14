import requests
from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        token = requests.post("http://127.0.0.1:8000/token/", data={"username": "admin", "password": "admin"})
        access = token.json()["access"]
        a = {"Authorization": "Bearer " + str(access)}
        self.client.get("/todo", headers=a)
        self.client.get("/hello", headers=a)
