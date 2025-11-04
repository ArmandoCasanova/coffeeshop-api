# Sistema de Inventario y Confirmación de Pago

## Descripción

Este sistema implementa el descuento automático de inventario de ingredientes cuando se confirma el pago de una orden.

## Flujo Completo

1. **Usuario crea orden** → Status: `pending`
2. **Usuario selecciona método de pago** → Actualiza `payment_type` (cash/card)
3. **Usuario confirma pago** → Endpoint `/orders/{id}/confirm-payment`
   - Valida que la orden existe y pertenece al usuario
   - Verifica que el status sea `pending`
   - Calcula ingredientes necesarios de todos los productos
   - Verifica stock disponible
   - Si hay stock suficiente: descuenta y cambia status a `paid`
   - Si no hay stock: retorna error 400 con detalle de ingredientes faltantes

## Estructura de Datos

### ProductModel - Campo `ingredients_json`

```json
{
  "ingredients": [
    {
      "ingredientId": "uuid-del-ingrediente",
      "quantity": 30,
      "unit": "ml"
    }
  ]
}
```

### OrderModel - Campo `items_summary_json`

Ya contiene la información de productos y cantidades:
```json
[
  {
    "product_id": "uuid",
    "product_name": "Latte",
    "quantity": 2,
    "price": 4.5,
    "customizations": {...}
  }
]
```

## Endpoints

### POST /orders/{order_id}/confirm-payment

Simula la confirmación de pago exitoso de una pasarela.

**Request:**
- Headers: `Authorization: Bearer <token>`
- Path param: `order_id` (UUID)

**Response Success (200):**
```json
{
  "success": true,
  "message": "Payment confirmed successfully",
  "order": {
    "orderId": "uuid",
    "status": "paid",
    ...
  },
  "inventory_deduction": {
    "success": true,
    "deducted_ingredients": [
      {
        "ingredient_id": "uuid",
        "ingredient_name": "Leche",
        "quantity_deducted": 400,
        "remaining_stock": 4600
      }
    ]
  }
}
```

**Response Error - Stock Insuficiente (400):**
```json
{
  "detail": {
    "message": "Stock insuficiente para completar la orden",
    "insufficient_ingredients": [
      {
        "ingredient_name": "Leche",
        "available": 100,
        "needed": 400
      }
    ]
  }
}
```

**Response Error - Orden no encontrada (404):**
```json
{
  "detail": "Order not found"
}
```

**Response Error - No es tu orden (403):**
```json
{
  "detail": "Access denied: not your order"
}
```

**Response Error - Status inválido (400):**
```json
{
  "detail": "Order cannot be paid. Current status: paid"
}
```

## Cómo Probar

### 1. Preparar Base de Datos

```sql
-- Ver ingredientes disponibles
SELECT ingredient_id, name, unit_of_measure, stock_current_level 
FROM ingredients;

-- Agregar ingredientes a un producto
UPDATE products
SET ingredients_json = '{
  "ingredients": [
    {
      "ingredientId": "tu-uuid-de-leche",
      "quantity": 200,
      "unit": "ml"
    },
    {
      "ingredientId": "tu-uuid-de-cafe",
      "quantity": 30,
      "unit": "ml"
    }
  ]
}'
WHERE name = 'Latte';

-- Verificar
SELECT name, ingredients_json FROM products WHERE name = 'Latte';
```

### 2. Crear una Orden (App Mobile)

1. Agregar productos al carrito
2. Ir a checkout
3. Crear orden → Status: `pending`
4. Anotar el `orderId` de la respuesta

### 3. Confirmar Pago (App Mobile)

**Opción A - Desde la pantalla de Orders:**
1. Ir a Orders
2. Ver orden pendiente
3. Presionar en la orden
4. Seleccionar método de pago (QR o Tarjeta)
5. Si seleccionas Tarjeta, te lleva a la pantalla de pago
6. Presionar "Confirmar Pago"

**Opción B - API directa (Postman/cURL):**
```bash
curl -X POST http://localhost:8000/api/v1/orders/{order_id}/confirm-payment \
  -H "Authorization: Bearer <tu-token>" \
  -H "Content-Type: application/json"
```

### 4. Verificar Descuento de Stock

```sql
-- Ver stock actual de ingredientes
SELECT name, stock_current_level, stock_optimal_level 
FROM ingredients;

-- Ver órdenes pagadas
SELECT order_id, status, order_date, total_amount, items_summary_json 
FROM orders 
WHERE status = 'paid' 
ORDER BY order_date DESC;
```

## Logs y Debugging

El sistema registra en consola:
- Ingredientes calculados por orden
- Stock disponible vs necesario
- Ingredientes descontados con cantidades
- Errores de stock insuficiente

Busca en los logs de Docker:
```bash
docker logs coffeeapp-fastapi-app --tail 100 | grep -i "stock\|ingredient\|payment"
```

## Casos de Prueba

### Caso 1: Pago Exitoso
- Stock suficiente
- Orden en estado pending
- Usuario es dueño de la orden
- **Resultado:** Status → paid, stock descontado

### Caso 2: Stock Insuficiente
- Uno o más ingredientes sin stock suficiente
- **Resultado:** Error 400 con detalle de ingredientes

### Caso 3: Orden Ya Pagada
- Orden en estado paid/delivered/cancelled
- **Resultado:** Error 400 "Order cannot be paid"

### Caso 4: Orden de Otro Usuario
- Usuario A intenta pagar orden de Usuario B
- **Resultado:** Error 403 "Access denied"

## Archivos Modificados

### Backend
- `app/models/catalog/product_model.py` - Added `ingredients_json`
- `app/services/inventory_service.py` - NEW - Stock deduction logic
- `app/api/orders/order_router.py` - Added `/confirm-payment` endpoint
- `app/api/orders/order_controller.py` - Added `confirm_payment` method
- `app/api/orders/order_service.py` - Added `confirm_payment` logic
- `migrations/versions/ffb0f42cff25_add_ingredients_json_to_products.py` - NEW

### Frontend Mobile
- `constants/urlPaths.ts` - Added `CONFIRM_PAYMENT` path
- `services/orderService.ts` - Added `confirmPayment` method
- `app/(mainpages)/order/payment.tsx` - Updated to use `confirmPayment`

## Próximos Pasos

1. **Agregar validación de ingredientes al crear productos** (Admin panel)
2. **Implementar alertas de stock bajo** cuando ingredientes lleguen a nivel crítico
3. **Historial de movimientos de inventario** para auditoría
4. **Integración con pasarela de pago real** (Stripe, PayPal, etc.)
5. **Manejo de reembolsos** que reintegre stock si se cancela una orden pagada
