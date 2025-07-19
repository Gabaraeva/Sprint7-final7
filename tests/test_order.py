import pytest
import requests
from configuration import BASE_URL


def base_order_payload():
    return {
        "firstName": "Иван",
        "lastName": "Петров",
        "address": "Москва, ул. Ленина, 1",
        "metroStation": 4,
        "phone": "+79111234567",
        "rentTime": 3,
        "deliveryDate": "2023-12-31",
        "comment": "Тестовый заказ"
    }


@pytest.mark.parametrize("colors", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
def test_create_order_with_colors(colors):
    payload = base_order_payload()
    payload["color"] = colors

    response = requests.post(f"{BASE_URL}/api/v1/orders", json=payload)
    assert response.status_code == 201
    assert "track" in response.json()


def test_get_orders_list():
    response = requests.get(f"{BASE_URL}/api/v1/orders")
    assert response.status_code == 200
    assert "orders" in response.json()
    assert isinstance(response.json()["orders"], list)
    assert len(response.json()["orders"]) > 0
# Updated: 2025-07-19 01:05:38
