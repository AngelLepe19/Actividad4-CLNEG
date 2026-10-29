## TechStore - Actividad 4 (Lógica de Negocio)

Este repositorio contiene la **Actividad 4** de la materia Componentes de Lógica de Negocio (FIME). Aquí desarrollamos el "cerebro" o núcleo de negocio de una tienda simulada usando Python, aplicando reglas de dominio y conectándolo a una API sencilla con FastAPI.

Integrantes:
| Alumno | Matrícula |
| :--- | :--- |
| Ángel Uriel Lepe Rodriguez | 2115842 |
| Eder Abihú López Guzmán | 2116464 |
| Alexia Guadalupe Rodriguez Lara | 2117441 |

Toda la información se maneja en memoria a través de unos archivos CSV de prueba (no requiere base de datos).

## Reglas del Negocio (Lo que hace el sistema)

Nuestro código se encarga de proteger las siguientes reglas de TechStore:
1. **Límite de artículos:** Un pedido no puede tener más de 20 unidades en total.
2. **Validación de estados:** Los artículos solo se pueden agregar si el pedido está en estado `DRAFT` (borrador).
3. **Descuento VIP (10%):** Se aplica solo si la compra supera los $500 MXN, el cliente es VIP, lleva al menos 4 unidades y no hay otra promoción activa.
4. **Descuento por Volumen (5%):** Se aplica si el total supera los $5,000 MXN y no hay otra promoción activa.
5. **Máquina de estados:** Los pedidos siguen un orden estricto (`DRAFT` ➔ `CONFIRMED` ➔ `SHIPPED`). No puedes enviar algo que no ha sido confirmado, ni cancelar algo que ya se envió.

## Pasos de Instalación

1. Clona este repositorio en tu computadora:
   ```bash
   git clone https://github.com/AngelLepe19/Actividad4-CLNEG
   cd Actividad4-CLNEG
   ```

2. Crea y activa un entorno virtual (para no mezclar librerías):
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Mac/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Instala las librerías necesarias:
   ```bash
   python -m pip install fastapi uvicorn pytest httpx
   ```

## Ejecución de la API y Pruebas

**Para levantar la API (Servidor):**
Ejecuta el siguiente comando en tu terminal:
```bash
uvicorn app.api:app --reload
```
Una vez iniciado, entra en tu navegador a **http://127.0.0.1:8000/docs** para ver y probar la interfaz (Swagger).

**Para correr las pruebas automáticas:**
Programamos pruebas para los 15 escenarios solicitados (E01 al E15). Para ejecutarlas, usa:
```bash
python -m pytest -q
```

## Endpoints de la API

La API cuenta con las siguientes rutas principales para gestionar los pedidos:

* **`GET /orders/{order_id}`**: Te muestra los detalles y el estado actual de un pedido.
* **`POST /orders/{order_id}/confirm`**: Confirma el pedido (solo si es válido).
* **`POST /orders/{order_id}/ship`**: Pasa el pedido a estado "Enviado" (te pedirá un número de guía).
* **`POST /orders/{order_id}/cancel`**: Cancela el pedido (te pedirá un motivo).

*Nota: La API está configurada para devolver errores claros si intentas romper las reglas (ej. Error 409 si intentas confirmar un pedido dos veces).*
