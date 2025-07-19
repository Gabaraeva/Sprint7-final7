import pytest
import requests
from helpers import register_new_courier, delete_courier, login_courier
from configuration import BASE_URL


def test_create_courier_success():
    courier = register_new_courier()
    assert courier is not None

    courier_id = login_courier(courier["login"], courier["password"])
    if courier_id:
        delete_response = delete_courier(courier_id)
        assert delete_response.status_code == 200


def test_create_duplicate_courier():
    courier = register_new_courier()

    payload = {
        "login": courier["login"],
        "password": "any_password",
        "firstName": "any_name"
    }

    response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload)
    assert response.status_code == 409
    assert "Этот логин уже используется" in response.json()["message"]

    courier_id = login_courier(courier["login"], courier["password"])
    if courier_id:
        delete_courier(courier_id)


@pytest.mark.parametrize("field", ["login", "password", "firstName"])
def test_create_courier_missing_field(field):
    payload = {
        "login": "test_login",
        "password": "test_pass",
        "firstName": "test_name"
    }
    del payload[field]

    response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload)
    assert response.status_code == 400
    assert "Недостаточно данных" in response.json()["message"]


def test_login_success():
    courier = register_new_courier()
    payload = {"login": courier["login"], "password": courier["password"]}
    response = requests.post(f"{BASE_URL}/api/v1/courier/login", json=payload)

    assert response.status_code == 200
    assert "id" in response.json()

    courier_id = response.json()["id"]
    delete_courier(courier_id)


def test_login_invalid_credentials():
    payload = {"login": "nonexistent_user", "password": "wrong_password"}
    response = requests.post(f"{BASE_URL}/api/v1/courier/login", json=payload)
    assert response.status_code == 404
    assert "Учетная запись не найдена" in response.json()["message"]
# Updated: 2025-07-19 01:05:38
