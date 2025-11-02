# Integración de Home - Productos Populares y Favoritos

## Resumen de Cambios

### Backend (API)

#### 1. Redis Cache Implementation
- **Archivo**: `app/core/redis_client.py` (NUEVO)
  - Cliente Redis asíncrono para caché
  - Métodos para get/set/delete JSON
  - TTL configurable

#### 2. Settings
- **Archivo**: `app/core/settings.py`
  - Agregada propiedad `REDIS_URL`
  - Función `get_settings()` para dependency injection

#### 3. Product Service
- **Archivo**: `app/api/products/product_service.py`
  - **Caché en `get_all_products`**: Productos disponibles se cachean por 1 hora
  - **Método `get_popular_products`**: 
    - Obtiene productos más vendidos de los últimos 7 días
    - Calcula desde `order_item` JOIN `orders`
    - Cachea resultados por 1 hora
  - **Método `get_user_favorite_products`**:
    - Obtiene favoritos desde tabla `user_favorites`
    - Cachea por usuario por 1 hora
  - **Invalidación de caché**: Al crear/actualizar/eliminar productos

#### 4. Product Controller
- **Archivo**: `app/api/products/product_controller.py`
  - `get_popular_products(limit)`: Endpoint para populares
  - `get_user_favorite_products(user_id, limit)`: Endpoint para favoritos

#### 5. Product Router
- **Archivo**: `app/api/products/product_router.py`
  - `GET /products/popular/list`: Productos populares
  - `GET /products/favorites/user/{user_id}`: Favoritos por usuario

#### 6. Auth Response
- **Archivo**: `app/api/auth/auth_schema.py`
  - `AuthResponseSchema` ya incluye `user_id`, `name`, `email`, etc.

#### 7. SQL Examples
- **Archivo**: `SQLProductsExample.sql`
  - Eliminadas referencias a `is_popular` e `is_favorite` de productos
  - Query para limpiar datos antiguos
  - Ejemplo de insert en `user_favorites`

#### 8. Requirements
- **Archivo**: `requirements.txt`
  - Agregado: `redis>=5.0.0`

---

### Frontend (UI)

#### 1. Models
- **Archivo**: `models/Product.ts` (NUEVO)
  - `TProduct`: Modelo completo de producto
  - `TCategoryInfo`: Sin `is_popular` ni `is_favorite`
  - `TCustomizationDetails`: Para opciones de personalización
  - `TProductListResponse`: Para respuestas paginadas

- **Archivo**: `models/Common.ts`
  - `TLoginTokens` actualizado con `user_id`, `name`, `email`, `role`, `is_verified`

#### 2. Constants
- **Archivo**: `constants/urlPaths.ts`
  - `PRODUCTS.GET_ALL`: Lista de productos
  - `PRODUCTS.GET_POPULAR`: Productos populares
  - `PRODUCTS.GET_USER_FAVORITES`: Favoritos por usuario

#### 3. Services
- **Archivo**: `services/products.ts` (NUEVO)
  - `getProducts(params)`: Obtener todos los productos
  - `getPopularProducts(limit)`: Obtener populares
  - `getUserFavoriteProducts(userId, limit)`: Obtener favoritos

#### 4. Hooks
- **Archivo**: `hooks/products/useGetProducts.ts` (NUEVO)
  - Hook genérico para obtener productos con React Query
  - Cache de 5 minutos (staleTime)
  - Garbage collection a los 10 minutos

- **Archivo**: `hooks/products/useGetPopularProducts.ts` (NUEVO)
  - Hook específico para productos populares
  - Llama al endpoint `/products/popular/list`

- **Archivo**: `hooks/products/useGetFavoriteProducts.ts` (NUEVO)
  - Hook específico para favoritos
  - Requiere `userId`
  - Solo se ejecuta si hay `userId` (enabled)

- **Archivo**: `hooks/auth/useLoginMutation.ts`
  - Guarda `userId`, `userName`, `userEmail`, `userRole` en AsyncStorage

#### 5. Screens
- **Archivo**: `app/(mainpages)/home.tsx`
  - Obtiene `userId` y `userName` de AsyncStorage
  - Usa `useGetPopularProducts()` para sección "Populares"
  - Usa `useGetFavoriteProducts(userId)` para sección "Favoritos"
  - Loading states con ActivityIndicator
  - Mensajes cuando no hay productos
  - Integración con ProductCard existente

---

## Flujo de Datos

### Productos Populares
1. Frontend llama a `useGetPopularProducts(10)`
2. React Query verifica caché local (5 min)
3. Si no hay caché, hace request a `/products/popular/list?limit=10`
4. Backend verifica caché Redis (1 hora)
5. Si no hay caché, calcula desde órdenes de últimos 7 días
6. Guarda en Redis y retorna productos
7. Frontend muestra en sección "Populares"

### Productos Favoritos
1. Frontend obtiene `userId` de AsyncStorage
2. Llama a `useGetFavoriteProducts(userId, 10)`
3. React Query verifica caché local (5 min)
4. Si no hay caché, hace request a `/products/favorites/user/{userId}?limit=10`
5. Backend verifica caché Redis por usuario (1 hora)
6. Si no hay caché, consulta tabla `user_favorites`
7. Guarda en Redis y retorna productos
8. Frontend muestra en sección "Favoritos"

---

## Optimizaciones de Performance

### Backend
1. **Redis Cache**: Reduce consultas a PostgreSQL en ~90%
2. **TTL de 1 hora**: Balance entre freshness y performance
3. **Invalidación inteligente**: Solo al modificar productos
4. **Índices**: `product_id`, `is_available`, timestamps
5. **Limit en queries**: Evita cargar toda la BD

### Frontend
1. **React Query Cache**: Evita re-fetching innecesario
2. **staleTime 5 min**: Datos frescos sin spam de requests
3. **gcTime 10 min**: Limpia memoria automáticamente
4. **enabled flag**: Solo fetch favoritos si hay userId
5. **Parallel queries**: Populares y favoritos se cargan simultáneamente

---

## Próximos Pasos

1. **Instalar dependencias**:
   ```bash
   # Backend
   cd coffeeshop-api
   pip install redis>=5.0.0
   
   # Frontend (si es necesario)
   cd coffeeshop-ui
   npm install
   ```

2. **Levantar Docker Compose** (incluye Redis):
   ```bash
   docker-compose up -d
   ```

3. **Limpiar datos antiguos** (si tienes productos con is_popular/is_favorite):
   ```sql
   UPDATE products 
   SET category_info_json = category_info_json - 'is_popular' - 'is_favorite'
   WHERE category_info_json ? 'is_popular' OR category_info_json ? 'is_favorite';
   ```

4. **Insertar productos de prueba**:
   - Usa `SQLProductsExample.sql`

5. **Agregar favoritos de prueba**:
   ```sql
   INSERT INTO user_favorites (user_id, product_id)
   VALUES ('tu-user-id', 'product-id')
   ON CONFLICT DO NOTHING;
   ```

6. **Probar la app**:
   - Login para obtener `userId`
   - Navegar a Home
   - Ver productos populares y favoritos

---

## Notas Importantes

- Los productos populares se calculan dinámicamente basados en ventas reales
- Los favoritos son específicos por usuario (tabla `user_favorites`)
- El caché se invalida automáticamente al modificar productos
- Si no hay órdenes recientes, la sección "Populares" estará vacía
- Si el usuario no tiene favoritos, esa sección estará vacía
