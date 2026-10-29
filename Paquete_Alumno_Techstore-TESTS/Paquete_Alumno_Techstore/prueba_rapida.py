from cargar_csv import load_fixture
from app.specifications import discount_rate

orders = load_fixture()
for oid in ["O001", "O002", "O005", "O006", "O010", "O011"]:
    print(oid, discount_rate(orders[oid]))