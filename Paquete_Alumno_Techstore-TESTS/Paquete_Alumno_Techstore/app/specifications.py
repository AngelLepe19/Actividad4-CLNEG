from decimal import Decimal


class Specification:
    def is_satisfied_by(self, order):
        raise NotImplementedError

    def __and__(self, other):
        return AndSpec(self, other)

    def __or__(self, other):
        return OrSpec(self, other)

    def __invert__(self):
        return NotSpec(self)


class AndSpec(Specification):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def is_satisfied_by(self, order):
        return (self.left.is_satisfied_by(order)
                and self.right.is_satisfied_by(order))


class OrSpec(Specification):
    def __init__(self, left, right):
        self.left, self.right = left, right

    def is_satisfied_by(self, order):
        return (self.left.is_satisfied_by(order)
                or self.right.is_satisfied_by(order))


class NotSpec(Specification):
    def __init__(self, spec):
        self.spec = spec

    def is_satisfied_by(self, order):
        return not self.spec.is_satisfied_by(order)


# ---------- Reglas concretas ----------
class MinimumAmountSpec(Specification):
    def __init__(self, minimum):
        self.minimum = minimum

    def is_satisfied_by(self, order):
        return order.total.amount > self.minimum      # estrictamente mayor


class VIPCustomerSpec(Specification):
    def is_satisfied_by(self, order):
        return order.customer.is_vip


class MinimumUnitsSpec(Specification):
    def __init__(self, minimum):
        self.minimum = minimum

    def is_satisfied_by(self, order):
        return order.units >= self.minimum            # 4 o más


class ActivePromotionSpec(Specification):
    def is_satisfied_by(self, order):
        return order.has_promotion


# ---------- Reglas de descuento ----------
TEN_PERCENT = (
    MinimumAmountSpec(Decimal("500"))
    & VIPCustomerSpec()
    & MinimumUnitsSpec(4)
    & ~ActivePromotionSpec()
)
FIVE_PERCENT = MinimumAmountSpec(Decimal("5000")) & ~ActivePromotionSpec()


def discount_rate(order):
    """Prioridad: si cumple ambas, se aplica el 10%."""
    if TEN_PERCENT.is_satisfied_by(order):
        return Decimal("0.10")
    if FIVE_PERCENT.is_satisfied_by(order):
        return Decimal("0.05")
    return Decimal("0")

HAS_DISCOUNT = TEN_PERCENT | FIVE_PERCENT