from decimal import Decimal
from cargar_csv import load_fixture
from app.domain import DomainException, OrderItem, Money


def ejecutar(caso, order, pasos):
    print(f"--- {caso} ({order.id}) estado inicial: {order.status.value}")
    for nombre, accion in pasos:
        try:
            accion()
            print(f"  {nombre}: OK -> {order.status.value}")
        except DomainException as e:
            print(f"  {nombre}: RECHAZADO {type(e).__name__}: {e}")
    print(f"  final: {order.status.value} | eventos: {[e.name for e in order.events]}")


o = load_fixture()
ejecutar("E03", o["O003"], [("confirm", o["O003"].confirm)])
ejecutar("E06", o["O007"], [("confirm", o["O007"].confirm)])
ejecutar("E07", o["O008"], [("confirm", o["O008"].confirm)])
ejecutar("E08", o["O009"], [("add_item SKU003 x2",
         lambda: o["O009"].add_item(OrderItem("SKU003", 2, Money(Decimal("120.00")))))])
ejecutar("E11", o["O012"], [("confirm", o["O012"].confirm),
                            ("ship sin guia", lambda: o["O012"].ship(""))])
ejecutar("E12", o["O013"], [("confirm 1", o["O013"].confirm),
                            ("confirm 2", o["O013"].confirm)])
ejecutar("E13", o["O014"], [("confirm", o["O014"].confirm),
                            ("ship", lambda: o["O014"].ship("GUIA-001")),
                            ("cancel", lambda: o["O014"].cancel("cliente cambió de opinión"))])
ejecutar("E14", o["O015"], [("confirm", o["O015"].confirm),
                            ("ship", lambda: o["O015"].ship("GUIA-002")),
                            ("return", o["O015"].return_order)])
ejecutar("E15", o["O016"], [("confirm", o["O016"].confirm),
                            ("ship", lambda: o["O016"].ship("GUIA-003")),
                            ("deliver", o["O016"].deliver)])