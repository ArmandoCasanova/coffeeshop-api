-- Ejemplo de INSERT de productos con la estructura correcta
-- Los productos populares se calculan dinámicamente basados en ventas de los últimos 7 días
-- Los favoritos se manejan en la tabla user_favorites por usuario

-- Producto 1: Caramel Frappé
INSERT INTO products (product_id, name, base_price, image_url, is_available, category_info_json, customization_details_json, created_at, updated_at)
VALUES (
  gen_random_uuid(),
  'Caramel Frappé',
  10.50,
  'https://example.com/images/caramel-frappe.jpg',
  true,
  '{
    "category_id": "cat-001",
    "category_name": "Frappé"
  }'::jsonb,
  '{
    "sizes": [
      {"size_name": "Pequeño", "size_price": 0},
      {"size_name": "Mediano", "size_price": 2},
      {"size_name": "Grande", "size_price": 4}
    ],
    "customization_groups": ["sugar_level", "ice_level", "toppings"]
  }'::jsonb,
  NOW(),
  NOW()
);

-- Producto 2: Mocha Latte
INSERT INTO products (product_id, name, base_price, image_url, is_available, category_info_json, customization_details_json, created_at, updated_at)
VALUES (
  gen_random_uuid(),
  'Mocha Latte',
  12.00,
  'https://example.com/images/mocha-latte.jpg',
  true,
  '{
    "category_id": "cat-002",
    "category_name": "Latte"
  }'::jsonb,
  '{
    "sizes": [
      {"size_name": "Pequeño", "size_price": 0},
      {"size_name": "Mediano", "size_price": 2},
      {"size_name": "Grande", "size_price": 4}
    ],
    "customization_groups": ["milk_type", "sugar_level", "temperature"]
  }'::jsonb,
  NOW(),
  NOW()
);

-- Producto 3: Espresso Shot
INSERT INTO products (product_id, name, base_price, image_url, is_available, category_info_json, customization_details_json, created_at, updated_at)
VALUES (
  gen_random_uuid(),
  'Espresso Shot',
  8.00,
  'https://example.com/images/espresso.jpg',
  true,
  '{
    "category_id": "cat-003",
    "category_name": "Espresso"
  }'::jsonb,
  '{
    "sizes": [
      {"size_name": "Simple", "size_price": 0},
      {"size_name": "Doble", "size_price": 3}
    ],
    "customization_groups": ["sugar_level"]
  }'::jsonb,
  NOW(),
  NOW()
);

-- Producto 4: Vanilla Frappé
INSERT INTO products (product_id, name, base_price, image_url, is_available, category_info_json, customization_details_json, created_at, updated_at)
VALUES (
  gen_random_uuid(),
  'Vanilla Frappé',
  11.00,
  'https://example.com/images/vanilla-frappe.jpg',
  true,
  '{
    "category_id": "cat-001",
    "category_name": "Frappé"
  }'::jsonb,
  '{
    "sizes": [
      {"size_name": "Pequeño", "size_price": 0},
      {"size_name": "Mediano", "size_price": 2},
      {"size_name": "Grande", "size_price": 4}
    ],
    "customization_groups": ["sugar_level", "ice_level", "toppings", "whipped_cream"]
  }'::jsonb,
  NOW(),
  NOW()
);

-- Producto 5: Chocolate Smoothie
INSERT INTO products (product_id, name, base_price, image_url, is_available, category_info_json, customization_details_json, created_at, updated_at)
VALUES (
  gen_random_uuid(),
  'Chocolate Smoothie',
  14.00,
  'https://example.com/images/chocolate-smoothie.jpg',
  true,
  '{
    "category_id": "cat-004",
    "category_name": "Smoothie"
  }'::jsonb,
  '{
    "sizes": [
      {"size_name": "Mediano", "size_price": 0},
      {"size_name": "Grande", "size_price": 3}
    ],
    "customization_groups": ["sugar_level", "protein_boost", "toppings"]
  }'::jsonb,
  NOW(),
  NOW()
);

-- Producto 6: Green Tea Latte
INSERT INTO products (product_id, name, base_price, image_url, is_available, category_info_json, customization_details_json, created_at, updated_at)
VALUES (
  gen_random_uuid(),
  'Green Tea Latte',
  9.50,
  'https://example.com/images/green-tea-latte.jpg',
  true,
  '{
    "category_id": "cat-005",
    "category_name": "Tés"
  }'::jsonb,
  '{
    "sizes": [
      {"size_name": "Pequeño", "size_price": 0},
      {"size_name": "Mediano", "size_price": 2},
      {"size_name": "Grande", "size_price": 4}
    ],
    "customization_groups": ["milk_type", "sugar_level", "temperature"]
  }'::jsonb,
  NOW(),
  NOW()
);

-- LIMPIAR productos existentes para eliminar is_popular e is_favorite si existen
-- Ejecutar este query si ya tienes productos en la BD con estas propiedades:

UPDATE products 
SET category_info_json = category_info_json - 'is_popular' - 'is_favorite'
WHERE category_info_json ? 'is_popular' OR category_info_json ? 'is_favorite';

-- Ejemplo para agregar productos a favoritos de un usuario:
-- INSERT INTO user_favorites (user_id, product_id)
-- VALUES ('user-uuid-aqui', 'product-uuid-aqui')
-- ON CONFLICT DO NOTHING;
