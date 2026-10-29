from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from cargar_csv import load_fixture
from app.domain import (
    InvalidOrderTransition, InvalidOrderData, OrderItemLimitExceeded,
)
from app.specifications import discount_rate

app = FastAPI(title="TechStore U4")
orders = load_fixture()


class ShipRequest(BaseModel):
    tracking_number: str


class CancelRequest(BaseModel):
    reason: str


def find_order(order_id: str):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido no existe")
    return order


def serialize(order):
    return {
        "id": order.id,
        "customer_id": order.customer.id,
        "status": order.status.value,
        "units": order.units,
        "total": str(order.total.amount),
        "discount_rate": str(discount_rate(order)),
        "tracking_number": order.tracking_number,
        "events": [e.name for e in order.events],
    }


def run(order_id: str, action):
    order = find_order(order_id)
    try:
        action(order)
    except InvalidOrderTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except (InvalidOrderData, OrderItemLimitExceeded) as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return serialize(order)


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    return serialize(find_order(order_id))


@app.post("/orders/{order_id}/confirm")
def confirm_order(order_id: str):
    return run(order_id, lambda o: o.confirm())


@app.post("/orders/{order_id}/ship")
def ship_order(order_id: str, body: ShipRequest):
    return run(order_id, lambda o: o.ship(body.tracking_number))


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str, body: CancelRequest):
    return run(order_id, lambda o: o.cancel(body.reason))


@app.post("/orders/{order_id}/deliver")
def deliver_order(order_id: str):
    return run(order_id, lambda o: o.deliver())


@app.post("/orders/{order_id}/return")
def return_order(order_id: str):
    return run(order_id, lambda o: o.return_order())