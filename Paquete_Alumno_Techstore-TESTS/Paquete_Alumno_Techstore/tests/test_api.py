import pytest
from fastapi.testclient import TestClient

from cargar_csv import load_fixture
from app import api


@pytest.fixture
def client():
    # Recarga los datos antes de cada prueba para que no se contaminen
    api.orders.clear()
    api.orders.update(load_fixture())
    return TestClient(api.app)


def test_get_pedido_200(client):
    r = client.get("/orders/O001")
    assert r.status_code == 200
    assert r.json()["total"] == "2100.00"
    assert r.json()["discount_rate"] == "0.10"


def test_pedido_inexistente_404(client):
    assert client.get("/orders/O999").status_code == 404


def test_confirmar_y_confirmar_de_nuevo(client):
    assert client.post("/orders/O013/confirm").status_code == 200
    assert client.post("/orders/O013/confirm").status_code == 409


def test_confirmar_pedido_vacio_422(client):
    assert client.post("/orders/O007/confirm").status_code == 422


def test_confirmar_cliente_inactivo_422(client):
    assert client.post("/orders/O003/confirm").status_code == 422


def test_enviar_sin_guia_422(client):
    client.post("/orders/O012/confirm")
    r = client.post("/orders/O012/ship", json={"tracking_number": ""})
    assert r.status_code == 422


def test_cancelar_desde_shipped_409(client):
    client.post("/orders/O014/confirm")
    client.post("/orders/O014/ship", json={"tracking_number": "GUIA-001"})
    r = client.post("/orders/O014/cancel", json={"reason": "x"})
    assert r.status_code == 409