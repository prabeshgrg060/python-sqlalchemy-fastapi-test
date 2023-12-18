from locust import HttpUser, task, between
import random
import string

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Time between task execution
    host = "http://127.0.0.1:8000"
    @task(1)
    def create_user(self):
        user_data = {
            "name": "".join(random.choices(string.ascii_letters, k=5)),
            "age":random.randint(18, 60) 
        }
        self.client.post("/user/", json=user_data)

    @task(2)
    def read_user(self):
        user_name = "ben"  # Change this to an existing user's name
        self.client.get(f"/user/{user_name}")
