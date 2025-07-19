import requests
import random
import string
from configuration import BASE_URL


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def register_new_courier():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload)

    if response.status_code == 201:
        return {
            "login": login,
            "password": password,
            "first_name": first_name
        }
    return None


def delete_courier(courier_id):
    return requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")


def login_courier(login, password):
    payload = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}/api/v1/courier/login", json=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None
# Updated: 2025-07-19 01:05:38
