
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ShopNest" in response.data


def test_health_api(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_products_api(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(response.json) > 0


def test_add_to_cart(client):
    response = client.post("/cart/add/1")
    assert response.status_code == 302

    cart = client.get("/cart")
    assert cart.json["items"][0]["quantity"] == 1


def test_invalid_product(client):
    response = client.post("/cart/add/999")
    assert response.status_code == 404
