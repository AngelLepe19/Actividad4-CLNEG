# TechStore U4 — Lógica de negocio con DDD

Proyecto de la Actividad 4 (Componentes de lógica de negocio, UANL FIME). Carga pedidos desde CSV a objetos de dominio, aplica reglas de descuento con Specifications, controla el ciclo de vida del pedido con una máquina de estados y eventos de dominio, y expone todo mediante una API REST con FastAPI.

## Requisitos
- Python 3.11 o superior

## Instalación (PowerShell, Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Si no tienes `requirements.txt`: `pip install fastapi uvicorn pytest httpx`

## Ejecutar la API
```powershell
python -m uvicorn app.api:app --reload
```
Abre http://127.0.0.1:8000/docs (Swagger) para probar los endpoints.

## Ejecutar pruebas
```powershell
python -m pytest -v
```
Resultado esperado: 25 pruebas aprobadas.

## Estructura
```
app/
  domain.py          Order, Money, OrderItem, Customer, eventos y excepciones
  specifications.py  Specifications (&, |, ~) y reglas de descuento
  api.py             API FastAPI
datos/               CSV de clientes, productos y pedidos
tests/               test_domain.py, test_api.py
prueba_rapida.py     Descuentos de pedidos de ejemplo
prueba_estados.py    Escenarios de estados (E03, E06-E08, E11-E15)
```

## Reglas de negocio
- Máximo 20 **unidades** por pedido (suma de cantidades, no de renglones).
- Descuento 10 %: cliente VIP, total > 500, al menos 4 unidades y sin promoción activa.
- Descuento 5 %: total > 5,000 y sin promoción activa. El 10 % tiene prioridad.
- Dinero con `Decimal`, moneda MXN.

## Estados del pedido
DRAFT → CONFIRMED → SHIPPED → DELIVERED / RETURNED; CONFIRMED → CANCELLED.
Cada transición valida, cambia el estado y registra el evento (OrderConfirmed, OrderShipped, OrderCancelled, OrderDelivered, OrderReturned).

## Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| GET | /orders/{order_id} | Consulta pedido, descuento y eventos |
| POST | /orders/{order_id}/confirm | Confirma |
| POST | /orders/{order_id}/ship | Envía (body: `tracking_number`) |
| POST | /orders/{order_id}/cancel | Cancela (body: `reason`) |
| POST | /orders/{order_id}/deliver | Entrega |
| POST | /orders/{order_id}/return | Devuelve |

Códigos de error: 404 pedido inexistente, 409 transición inválida, 422 datos inválidos o límite de unidades.

## Notas
- Los datos viven en memoria: reiniciar el servidor restaura los pedidos en DRAFT.
- IDs de pedido con letra O: `O001`, no `1`.

**Autor:** Eder Abihú López Guzmán — Equipo 4
