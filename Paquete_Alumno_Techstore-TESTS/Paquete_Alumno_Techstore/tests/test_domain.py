import pytest
from decimal import Decimal

from cargar_csv import load_fixture
from app.domain import (
    Money, OrderItem, OrderStatus,
    InvalidOrderData, InvalidOrderTransition, OrderItemLimitExceeded,
)
from app.specifications import discount_rate


@pytest.fixture
def orders():
    return load_fixture()


# ---------- Money ----------
def test_money_negativo():
    with pytest.raises(InvalidOrderData):
        Money(Decimal("-1"))


def test_money_monedas_distintas():
    with pytest.raises(InvalidOrderData):
        Money(Decimal("1")).add(Money(Decimal("1"), "USD"))


# ---------- Carga y límites ----------
def test_o001_carga_correcta(orders):
    o = orders["O001"]
    assert o.status == OrderStatus.DRAFT
    assert o.units == 4
    assert o.total.amount == Decimal("2100.00")


def test_21_unidades_rechazadas(orders):
    o = orders["O009"]  # ya tiene 19
    with pytest.raises(OrderItemLimitExceeded):
        o.add_item(OrderItem("SKU003", 2, Money(Decimal("120.00"))))
    assert o.units == 19


def test_20_unidades_permitidas(orders):
    o = orders["O008"]
    assert o.units == 20
    o.confirm()
    assert o.status == OrderStatus.CONFIRMED


# ---------- Confirmación ----------
def test_cliente_inactivo_no_confirma(orders):
    o = orders["O003"]
    with pytest.raises(InvalidOrderData):
        o.confirm()
    assert o.status == OrderStatus.DRAFT
    assert o.events == []


def test_pedido_vacio_no_confirma(orders):
    o = orders["O007"]
    with pytest.raises(InvalidOrderData):
        o.confirm()
    assert o.events == []


# ---------- Descuentos ----------
@pytest.mark.parametrize("oid, esperado", [
    ("O001", "0.10"),   # VIP, 4 unidades, >500, sin promo
    ("O002", "0"),      # no VIP, total < 5000
    ("O005", "0"),      # promoción activa
    ("O006", "0.05"),   # total > 5000
    ("O010", "0"),      # total exactamente 500
    ("O011", "0"),      # solo 3 unidades
])
def test_descuento(orders, oid, esperado):
    assert discount_rate(orders[oid]) == Decimal(esperado)


# ---------- Transiciones y eventos ----------
def test_envio_sin_guia(orders):
    o = orders["O012"]
    o.confirm()
    with pytest.raises(InvalidOrderData):
        o.ship("")
    assert o.status == OrderStatus.CONFIRMED
    assert [e.name for e in o.events] == ["OrderConfirmed"]


def test_confirmacion_doble(orders):
    o = orders["O013"]
    o.confirm()
    with pytest.raises(InvalidOrderTransition):
        o.confirm()
    assert len(o.events) == 1


def test_cancelar_desde_shipped(orders):
    o = orders["O014"]
    o.confirm()
    o.ship("GUIA-001")
    with pytest.raises(InvalidOrderTransition):
        o.cancel("ya no lo quiero")
    assert o.status == OrderStatus.SHIPPED


def test_devolucion(orders):
    o = orders["O015"]
    o.confirm()
    o.ship("GUIA-002")
    o.return_order()
    assert o.status == OrderStatus.RETURNED
    assert o.events[-1].name == "OrderReturned"


def test_entrega(orders):
    o = orders["O016"]
    o.confirm()
    o.ship("GUIA-003")
    o.deliver()
    assert o.status == OrderStatus.DELIVERED
    assert o.events[-1].name == "OrderDelivered"

from cargar_csv import load_fixture
from app.specifications import HAS_DISCOUNT


def test_tiene_algun_descuento_con_or():
    orders = load_fixture()
    assert HAS_DISCOUNT.is_satisfied_by(orders["O001"])      # 10 %
    assert HAS_DISCOUNT.is_satisfied_by(orders["O006"])      # 5 %
    assert not HAS_DISCOUNT.is_satisfied_by(orders["O002"])  # ninguno
    assert not HAS_DISCOUNT.is_satisfied_by(orders["O005"])  # promoción activa