

-- =============================================
-- 1. USUARIOS (Password para todos: "Test123!")
-- =============================================
INSERT INTO users (user_id, role, name, last_name, email, password, points, is_verified, birth_date, created_at, updated_at) VALUES
('10000000-0000-0000-0000-000000000001', 'admin', 'Alex', 'Admin', 'admin@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 0.00, TRUE, '1985-05-15', NOW(), NOW()),
('10000000-0000-0000-0000-000000000002', 'staff', 'Sara', 'Staff', 'staff@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 0.00, TRUE, '1992-11-20', NOW(), NOW()),
('10000000-0000-0000-0000-000000000003', 'customer', 'Armando', 'Casanova', 'armando@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 150.00, TRUE, '1995-03-10', NOW(), NOW()),
('10000000-0000-0000-0000-000000000004', 'customer', 'Brenda', 'Lopez', 'brenda@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 85.00, TRUE, '1998-07-25', NOW(), NOW()),
('10000000-0000-0000-0000-000000000005', 'customer', 'Carlos', 'Martinez', 'carlos@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 25.00, TRUE, '2000-12-01', NOW(), NOW());

-- =============================================
-- 2. CATEGORÍAS DE PRODUCTOS
-- =============================================
INSERT INTO product_categories (category_id, name, description, created_at, updated_at) VALUES
('50000000-0000-0000-0000-000000000001', 'Frappés', 'Bebidas frías mezcladas con hielo', NOW(), NOW()),
('50000000-0000-0000-0000-000000000002', 'Bebidas Calientes', 'Cafés y bebidas calientes', NOW(), NOW()),
('50000000-0000-0000-0000-000000000003', 'Panadería', 'Postres y bocadillos', NOW(), NOW()),
('50000000-0000-0000-0000-000000000004', 'Té y Tisanas', 'Infusiones naturales', NOW(), NOW()),
('50000000-0000-0000-0000-000000000005', 'Bebidas Frías', 'Bebidas frías sin hielo', NOW(), NOW());

-- =============================================


INSERT INTO products (product_id, name, description, base_price, image_url, is_available, category_info_json, customization_details_json, ingredients_json, created_at, updated_at) VALUES
('60000000-0000-0000-0000-000000000001', 'Caramel Frappé', 'Deliciosa bebida fría con caramelo y hielo frappe', 65.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000001", "category_name": "Frappés"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 10, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 15, "details": "310ml"}]}, "extras": {"group_id": "30000000-0000-0000-0000-000000000003", "system_name": "extras", "display_name": "Extras", "options": [{"option_id": "40000000-0000-0000-0000-000000000009", "name": "Extra Crema Batida", "extra_cost": 15, "details": "+50g crema"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000005", "quantity": 100, "unit": "g"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000002', 'Mocha Frappé', 'Frappé de chocolate y café con crema batida', 70.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000001", "category_name": "Frappés"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 10, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 15, "details": "310ml"}]}, "extras": {"group_id": "30000000-0000-0000-0000-000000000003", "system_name": "extras", "display_name": "Extras", "options": [{"option_id": "40000000-0000-0000-0000-000000000009", "name": "Extra Crema Batida", "extra_cost": 15, "details": "+50g crema"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000005", "quantity": 100, "unit": "g"}, {"ingredientId": "20000000-0000-0000-0000-000000000006", "quantity": 30, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000003', 'Vanilla Frappé', 'Refrescante frappé de vainilla con hielo', 60.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000001", "category_name": "Frappés"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 10, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 15, "details": "310ml"}]}, "extras": {"group_id": "30000000-0000-0000-0000-000000000003", "system_name": "extras", "display_name": "Extras", "options": [{"option_id": "40000000-0000-0000-0000-000000000009", "name": "Extra Crema Batida", "extra_cost": 15, "details": "+50g crema"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000005", "quantity": 100, "unit": "g"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000004', 'Strawberry Frappé', 'Frappé de fresa natural con hielo y crema', 68.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000001", "category_name": "Frappés"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 10, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 15, "details": "310ml"}]}, "extras": {"group_id": "30000000-0000-0000-0000-000000000003", "system_name": "extras", "display_name": "Extras", "options": [{"option_id": "40000000-0000-0000-0000-000000000009", "name": "Extra Crema Batida", "extra_cost": 15, "details": "+50g crema"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000005", "quantity": 100, "unit": "g"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000005', 'Cookies & Cream Frappé', 'Frappé con galletas Oreo trituradas y crema', 75.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000001", "category_name": "Frappés"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 10, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 15, "details": "310ml"}]}, "extras": {"group_id": "30000000-0000-0000-0000-000000000003", "system_name": "extras", "display_name": "Extras", "options": [{"option_id": "40000000-0000-0000-0000-000000000009", "name": "Extra Crema Batida", "extra_cost": 15, "details": "+50g crema"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000005", "quantity": 100, "unit": "g"}]}', NOW(), NOW());

INSERT INTO products (product_id, name, description, base_price, image_url, is_available, category_info_json, customization_details_json, ingredients_json, created_at, updated_at) VALUES
('60000000-0000-0000-0000-000000000006', 'Latte', 'Café espresso con leche vaporizada suave', 45.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000002", "category_name": "Bebidas Calientes"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}, "milk_type": {"group_id": "30000000-0000-0000-0000-000000000002", "system_name": "milk_type", "display_name": "Tipo de Leche", "options": [{"option_id": "40000000-0000-0000-0000-000000000004", "name": "Leche Entera", "extra_cost": 0, "details": "Base"}, {"option_id": "40000000-0000-0000-0000-000000000005", "name": "Leche de Almendras", "extra_cost": 12, "details": "+$12"}, {"option_id": "40000000-0000-0000-0000-000000000006", "name": "Deslactosada", "extra_cost": 8, "details": "+$8"}]}, "coffee_type": {"group_id": "30000000-0000-0000-0000-000000000004", "system_name": "coffee_type", "display_name": "Tipo de Café", "options": [{"option_id": "40000000-0000-0000-0000-000000000007", "name": "Regular", "extra_cost": 0, "details": "Base"}, {"option_id": "40000000-0000-0000-0000-000000000008", "name": "Descafeinado", "extra_cost": 0, "details": "Sin cargo"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000004", "quantity": 1, "unit": "shot"}, {"ingredientId": "20000000-0000-0000-0000-000000000002", "quantity": 160, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000007', 'Cappuccino', 'Café espresso con leche vaporizada y espuma', 48.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000002", "category_name": "Bebidas Calientes"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}, "milk_type": {"group_id": "30000000-0000-0000-0000-000000000002", "system_name": "milk_type", "display_name": "Tipo de Leche", "options": [{"option_id": "40000000-0000-0000-0000-000000000004", "name": "Leche Entera", "extra_cost": 0, "details": "Base"}, {"option_id": "40000000-0000-0000-0000-000000000005", "name": "Leche de Almendras", "extra_cost": 12, "details": "+$12"}, {"option_id": "40000000-0000-0000-0000-000000000006", "name": "Deslactosada", "extra_cost": 8, "details": "+$8"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000004", "quantity": 1, "unit": "shot"}, {"ingredientId": "20000000-0000-0000-0000-000000000002", "quantity": 100, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000008', 'Americano', 'Café espresso diluido en agua caliente', 38.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000002", "category_name": "Bebidas Calientes"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}, "coffee_type": {"group_id": "30000000-0000-0000-0000-000000000004", "system_name": "coffee_type", "display_name": "Tipo de Café", "options": [{"option_id": "40000000-0000-0000-0000-000000000007", "name": "Regular", "extra_cost": 0, "details": "Base"}, {"option_id": "40000000-0000-0000-0000-000000000008", "name": "Descafeinado", "extra_cost": 0, "details": "Sin cargo"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000004", "quantity": 2, "unit": "shot"}, {"ingredientId": "20000000-0000-0000-0000-000000000001", "quantity": 100, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000009', 'Espresso', 'Shot concentrado de café espresso', 35.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000002", "category_name": "Bebidas Calientes"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Simple", "extra_cost": 0, "details": "1 shot"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Doble", "extra_cost": 10, "details": "2 shots"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000004", "quantity": 1, "unit": "shot"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000010', 'Flat White', 'Café espresso con leche vaporizada y microespuma', 52.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000002", "category_name": "Bebidas Calientes"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}, "milk_type": {"group_id": "30000000-0000-0000-0000-000000000002", "system_name": "milk_type", "display_name": "Tipo de Leche", "options": [{"option_id": "40000000-0000-0000-0000-000000000004", "name": "Leche Entera", "extra_cost": 0, "details": "Base"}, {"option_id": "40000000-0000-0000-0000-000000000005", "name": "Leche de Almendras", "extra_cost": 12, "details": "+$12"}, {"option_id": "40000000-0000-0000-0000-000000000006", "name": "Deslactosada", "extra_cost": 8, "details": "+$8"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000004", "quantity": 1, "unit": "shot"}, {"ingredientId": "20000000-0000-0000-0000-000000000002", "quantity": 120, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000011', 'Hot Chocolate', 'Bebida caliente de chocolate y leche', 42.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000002", "category_name": "Bebidas Calientes"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000006", "quantity": 30, "unit": "ml"}, {"ingredientId": "20000000-0000-0000-0000-000000000002", "quantity": 200, "unit": "ml"}]}', NOW(), NOW());


INSERT INTO products (product_id, name, description, base_price, image_url, is_available, category_info_json, customization_details_json, ingredients_json, created_at, updated_at) VALUES
('60000000-0000-0000-0000-000000000012', 'Croissant', 'Crujiente panecillo francés de mantequilla', 35.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000003", "category_name": "Panadería"}', '{}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000008", "quantity": 1, "unit": "unidad"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000013', 'Panqué de Plátano', 'Bizcocho húmedo de plátano natural', 40.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000003", "category_name": "Panadería"}', '{}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000008", "quantity": 1, "unit": "unidad"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000014', 'Muffin de Chocolate', 'Muffin esponjoso con trozos de chocolate', 38.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000003", "category_name": "Panadería"}', '{}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000008", "quantity": 1, "unit": "unidad"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000015', 'Cookie con Chispas', 'Galleta horneada con chispas de chocolate', 32.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000003", "category_name": "Panadería"}', '{}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000008", "quantity": 1, "unit": "unidad"}]}', NOW(), NOW());


INSERT INTO products (product_id, name, description, base_price, image_url, is_available, category_info_json, customization_details_json, ingredients_json, created_at, updated_at) VALUES
('60000000-0000-0000-0000-000000000016', 'Green Tea Latte', 'Latte de té verde con leche vaporizada', 50.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000004", "category_name": "Té y Tisanas"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000010", "quantity": 5, "unit": "g"}, {"ingredientId": "20000000-0000-0000-0000-000000000002", "quantity": 200, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000017', 'Chai Latte', 'Bebida especiada de té negro con leche', 48.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000004", "category_name": "Té y Tisanas"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000010", "quantity": 5, "unit": "g"}, {"ingredientId": "20000000-0000-0000-0000-000000000002", "quantity": 180, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000018', 'Iced Coffee', 'Café frío servido con hielo', 40.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000005", "category_name": "Bebidas Frías"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000004", "quantity": 2, "unit": "shot"}, {"ingredientId": "20000000-0000-0000-0000-000000000001", "quantity": 150, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000019', 'Cold Brew', 'Café infusionado en frío por varias horas', 45.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000005", "category_name": "Bebidas Frías"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000004", "quantity": 2, "unit": "shot"}, {"ingredientId": "20000000-0000-0000-0000-000000000001", "quantity": 200, "unit": "ml"}]}', NOW(), NOW()),
('60000000-0000-0000-0000-000000000020', 'Lemonade', 'Refrescante limonada natural con hielo', 35.00, 'https://images.unsplash.com/photo-1630040995437-80b01c5dd52d?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDE3fHx8ZW58MHx8fHx8', TRUE, '{"category_id": "50000000-0000-0000-0000-000000000005", "category_name": "Bebidas Frías"}', '{"sizes": {"group_id": "30000000-0000-0000-0000-000000000001", "system_name": "size", "display_name": "Tamaño", "options": [{"option_id": "40000000-0000-0000-0000-000000000001", "name": "Chico", "extra_cost": 0, "details": "160ml"}, {"option_id": "40000000-0000-0000-0000-000000000002", "name": "Mediano", "extra_cost": 8, "details": "250ml"}, {"option_id": "40000000-0000-0000-0000-000000000003", "name": "Grande", "extra_cost": 12, "details": "310ml"}]}}', '{"ingredients": [{"ingredientId": "20000000-0000-0000-0000-000000000001", "quantity": 250, "unit": "ml"}]}', NOW(), NOW());

-- =============================================
-- INGREDIENTES (INVENTARIO)
-- =============================================
INSERT INTO ingredients (ingredient_id, name, unit_of_measure, stock_current_level, stock_optimal_level, created_at, updated_at) VALUES
('20000000-0000-0000-0000-000000000001', 'Agua Filtrada', 'ml', 50000, 30000, NOW(), NOW()),
('20000000-0000-0000-0000-000000000002', 'Leche Entera Base', 'ml', 15000, 10000, NOW(), NOW()),
('20000000-0000-0000-0000-000000000003', 'Leche de Almendras', 'ml', 8000, 5000, NOW(), NOW()),
('20000000-0000-0000-0000-000000000004', 'Café Espresso Regular', 'shot', 200, 150, NOW(), NOW()),
('20000000-0000-0000-0000-000000000005', 'Base Frappe Vainilla', 'g', 5000, 3000, NOW(), NOW()),
('20000000-0000-0000-0000-000000000006', 'Jarabe Chocolate', 'ml', 3000, 2000, NOW(), NOW()),
('20000000-0000-0000-0000-000000000007', 'Crema Batida', 'g', 1000, 500, NOW(), NOW()),
('20000000-0000-0000-0000-000000000008', 'Panqué Base', 'unidad', 20, 15, NOW(), NOW()),
('20000000-0000-0000-0000-000000000009', 'Café Espresso Descafeinado', 'shot', 100, 50, NOW(), NOW()),
('20000000-0000-0000-0000-000000000010', 'Té Negro Granel', 'g', 500, 300, NOW(), NOW()),
('20000000-0000-0000-0000-000000000011', 'Leche Deslactosada', 'ml', 5000, 3000, NOW(), NOW());

-- =============================================
-- GRUPOS DE PERSONALIZACIÓN
-- =============================================
INSERT INTO customization_groups (group_id, system_name, display_name, created_at, updated_at) VALUES
('30000000-0000-0000-0000-000000000001', 'size', 'Tamaño', NOW(), NOW()),
('30000000-0000-0000-0000-000000000002', 'milk_type', 'Tipo de Leche', NOW(), NOW()),
('30000000-0000-0000-0000-000000000003', 'extras', 'Extras', NOW(), NOW()),
('30000000-0000-0000-0000-000000000004', 'coffee_type', 'Tipo de Café', NOW(), NOW()),
('30000000-0000-0000-0000-000000000005', 'sweetener', 'Endulzante', NOW(), NOW());

-- =============================================
-- OPCIONES DE PERSONALIZACIÓN
-- =============================================
INSERT INTO customization_options (option_id, group_id, name, extra_cost, is_size_option, consumed_ingredient_id, quantity_consumed, details, created_at, updated_at) VALUES
-- GRUPO TAMAÑO
('40000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', 'Chico', 0.00, TRUE, NULL, 0.00, '160ml (Base)', NOW(), NOW()),
('40000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001', 'Mediano', 5.00, TRUE, '20000000-0000-0000-0000-000000000002', 90.00, '250ml', NOW(), NOW()),
('40000000-0000-0000-0000-000000000003', '30000000-0000-0000-0000-000000000001', 'Grande', 10.00, TRUE, '20000000-0000-0000-0000-000000000002', 150.00, '310ml', NOW(), NOW()),

-- GRUPO LECHE
('40000000-0000-0000-0000-000000000004', '30000000-0000-0000-0000-000000000002', 'Leche Entera', 0.00, FALSE, '20000000-0000-0000-0000-000000000002', 0.00, 'Base', NOW(), NOW()),
('40000000-0000-0000-0000-000000000005', '30000000-0000-0000-0000-000000000002', 'Leche de Almendras', 12.00, FALSE, '20000000-0000-0000-0000-000000000003', 0.00, '+$12', NOW(), NOW()),
('40000000-0000-0000-0000-000000000006', '30000000-0000-0000-0000-000000000002', 'Deslactosada', 8.00, FALSE, '20000000-0000-0000-0000-000000000011', 0.00, '+$8', NOW(), NOW()),

-- GRUPO CAFÉ
('40000000-0000-0000-0000-000000000007', '30000000-0000-0000-0000-000000000004', 'Regular', 0.00, FALSE, '20000000-0000-0000-0000-000000000004', 0.00, 'Base', NOW(), NOW()),
('40000000-0000-0000-0000-000000000008', '30000000-0000-0000-0000-000000000004', 'Descafeinado', 0.00, FALSE, '20000000-0000-0000-0000-000000000009', 0.00, 'Sin cargo', NOW(), NOW()),

-- GRUPO EXTRA
('40000000-0000-0000-0000-000000000009', '30000000-0000-0000-0000-000000000003', 'Extra Crema Batida', 15.00, FALSE, '20000000-0000-0000-0000-000000000007', 50.00, '+50g crema', NOW(), NOW());

-- =============================================
-- RECETAS BASE (product_ingredients)
-- =============================================
INSERT INTO product_ingredients (product_id, ingredient_id, quantity_required, created_at, updated_at) VALUES
-- Latte
('60000000-0000-0000-0000-000000000006', '20000000-0000-0000-0000-000000000004', 1.0, NOW(), NOW()), -- 1 shot espresso
('60000000-0000-0000-0000-000000000006', '20000000-0000-0000-0000-000000000002', 160.0, NOW(), NOW()), -- 160ml leche

-- Cappuccino
('60000000-0000-0000-0000-000000000007', '20000000-0000-0000-0000-000000000004', 1.0, NOW(), NOW()),
('60000000-0000-0000-0000-000000000007', '20000000-0000-0000-0000-000000000002', 100.0, NOW(), NOW()),

-- Americano
('60000000-0000-0000-0000-000000000008', '20000000-0000-0000-0000-000000000004', 2.0, NOW(), NOW()),
('60000000-0000-0000-0000-000000000008', '20000000-0000-0000-0000-000000000001', 100.0, NOW(), NOW()),

-- Frappés (Base Frappe)
('60000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000005', 100.0, NOW(), NOW()),
('60000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000005', 100.0, NOW(), NOW()),
('60000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000006', 30.0, NOW(), NOW()), -- Jarabe chocolate

-- Panadería
('60000000-0000-0000-0000-000000000012', '20000000-0000-0000-0000-000000000008', 1.0, NOW(), NOW()),
('60000000-0000-0000-0000-000000000013', '20000000-0000-0000-0000-000000000008', 1.0, NOW(), NOW());

-- =============================================
-- VINCULACIÓN PERSONALIZACIÓN-PRODUCTOS (product_customization_groups)
-- =============================================
INSERT INTO product_customization_groups (product_id, group_id) VALUES
-- Frappés: Tamaño y Extras
('60000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000003'),
('60000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000003'),
('60000000-0000-0000-0000-000000000003', '30000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000004', '30000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000005', '30000000-0000-0000-0000-000000000001'),

-- Bebidas Calientes: Tamaño, Leche, Tipo de Café
('60000000-0000-0000-0000-000000000006', '30000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000006', '30000000-0000-0000-0000-000000000002'),
('60000000-0000-0000-0000-000000000006', '30000000-0000-0000-0000-000000000004'),
('60000000-0000-0000-0000-000000000007', '30000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000007', '30000000-0000-0000-0000-000000000002'),
('60000000-0000-0000-0000-000000000008', '30000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000008', '30000000-0000-0000-0000-000000000004');

-- =============================================
-- VINCULACIÓN CATEGORÍAS (product_category_link)
-- =============================================
INSERT INTO product_category_link (product_id, category_id) VALUES
-- Frappés
('60000000-0000-0000-0000-000000000001', '50000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000002', '50000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000003', '50000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000004', '50000000-0000-0000-0000-000000000001'),
('60000000-0000-0000-0000-000000000005', '50000000-0000-0000-0000-000000000001'),

-- Bebidas Calientes
('60000000-0000-0000-0000-000000000006', '50000000-0000-0000-0000-000000000002'),
('60000000-0000-0000-0000-000000000007', '50000000-0000-0000-0000-000000000002'),
('60000000-0000-0000-0000-000000000008', '50000000-0000-0000-0000-000000000002'),
('60000000-0000-0000-0000-000000000009', '50000000-0000-0000-0000-000000000002'),
('60000000-0000-0000-0000-000000000010', '50000000-0000-0000-0000-000000000002'),
('60000000-0000-0000-0000-000000000011', '50000000-0000-0000-0000-000000000002'),

-- Panadería
('60000000-0000-0000-0000-000000000012', '50000000-0000-0000-0000-000000000003'),
('60000000-0000-0000-0000-000000000013', '50000000-0000-0000-0000-000000000003'),
('60000000-0000-0000-0000-000000000014', '50000000-0000-0000-0000-000000000003'),
('60000000-0000-0000-0000-000000000015', '50000000-0000-0000-0000-000000000003'),

-- Té y Tisanas
('60000000-0000-0000-0000-000000000016', '50000000-0000-0000-0000-000000000004'),
('60000000-0000-0000-0000-000000000017', '50000000-0000-0000-0000-000000000004'),

-- Bebidas Frías
('60000000-0000-0000-0000-000000000018', '50000000-0000-0000-0000-000000000005'),
('60000000-0000-0000-0000-000000000019', '50000000-0000-0000-0000-000000000005'),
('60000000-0000-0000-0000-000000000020', '50000000-0000-0000-0000-000000000005');

-- =============================================
-- 4. ÓRDENES DE LOS ÚLTIMOS 7 DÍAS (para productos populares)
-- =============================================

-- Órdenes hace 2 días (29 Oct 2025)
INSERT INTO orders (order_id, user_id, order_date, status, total_amount, points_earned, payment_type, items_summary_json, created_at, updated_at) VALUES
('70000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000003', NOW() - INTERVAL '2 days', 'paid', 145.00, 14.50, 'card', '[{"name": "Mocha Frappé", "qty": 2}]', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
('70000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000004', NOW() - INTERVAL '2 days', 'paid', 85.00, 8.50, 'card', '[{"name": "Latte", "qty": 1}, {"name": "Croissant", "qty": 1}]', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days');

-- Order Items hace 2 días
INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase, created_at, updated_at) VALUES
('80000000-0000-0000-0000-000000000001', '70000000-0000-0000-0000-000000000001', '60000000-0000-0000-0000-000000000002', 2, 70.00, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'), -- Mocha Frappé x2
('80000000-0000-0000-0000-000000000002', '70000000-0000-0000-0000-000000000002', '60000000-0000-0000-0000-000000000006', 1, 45.00, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'), -- Latte
('80000000-0000-0000-0000-000000000003', '70000000-0000-0000-0000-000000000002', '60000000-0000-0000-0000-000000000012', 1, 35.00, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'); -- Croissant

-- Órdenes hace 3 días (28 Oct 2025)
INSERT INTO orders (order_id, user_id, order_date, status, total_amount, points_earned, payment_type, items_summary_json, created_at, updated_at) VALUES
('70000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000005', NOW() - INTERVAL '3 days', 'paid', 175.00, 17.50, 'card', '[{"name": "Caramel Frappé", "qty": 1}, {"name": "Cappuccino", "qty": 2}]', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
('70000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000003', NOW() - INTERVAL '3 days', 'paid', 120.00, 12.00, 'cash', '[{"name": "Mocha Frappé", "qty": 1}, {"name": "Panqué", "qty": 1}]', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days');

-- Order Items hace 3 días
INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase, created_at, updated_at) VALUES
('80000000-0000-0000-0000-000000000004', '70000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000001', 1, 65.00, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'), -- Caramel Frappé
('80000000-0000-0000-0000-000000000005', '70000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000007', 2, 48.00, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'), -- Cappuccino x2
('80000000-0000-0000-0000-000000000006', '70000000-0000-0000-0000-000000000004', '60000000-0000-0000-0000-000000000002', 1, 70.00, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'), -- Mocha Frappé
('80000000-0000-0000-0000-000000000007', '70000000-0000-0000-0000-000000000004', '60000000-0000-0000-0000-000000000013', 1, 40.00, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'); -- Panqué

-- Órdenes hace 4 días (27 Oct 2025)
INSERT INTO orders (order_id, user_id, order_date, status, total_amount, points_earned, payment_type, items_summary_json, created_at, updated_at) VALUES
('70000000-0000-0000-0000-000000000005', '10000000-0000-0000-0000-000000000004', NOW() - INTERVAL '4 days', 'paid', 208.00, 20.80, 'card', '[{"name": "Latte", "qty": 3}, {"name": "Cookie", "qty": 2}]', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
('70000000-0000-0000-0000-000000000006', '10000000-0000-0000-0000-000000000005', NOW() - INTERVAL '4 days', 'paid', 95.00, 9.50, 'card', '[{"name": "Americano", "qty": 2}]', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days');

-- Order Items hace 4 días
INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase, created_at, updated_at) VALUES
('80000000-0000-0000-0000-000000000008', '70000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000006', 3, 45.00, NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'), -- Latte x3
('80000000-0000-0000-0000-000000000009', '70000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000015', 2, 32.00, NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'), -- Cookie x2
('80000000-0000-0000-0000-000000000010', '70000000-0000-0000-0000-000000000006', '60000000-0000-0000-0000-000000000008', 2, 38.00, NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'); -- Americano x2

-- Órdenes hace 5 días (26 Oct 2025)
INSERT INTO orders (order_id, user_id, order_date, status, total_amount, points_earned, payment_type, items_summary_json, created_at, updated_at) VALUES
('70000000-0000-0000-0000-000000000007', '10000000-0000-0000-0000-000000000003', NOW() - INTERVAL '5 days', 'paid', 155.00, 15.50, 'card', '[{"name": "Caramel Frappé", "qty": 2}, {"name": "Muffin", "qty": 1}]', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
('70000000-0000-0000-0000-000000000008', '10000000-0000-0000-0000-000000000004', NOW() - INTERVAL '5 days', 'paid', 130.00, 13.00, 'cash', '[{"name": "Cappuccino", "qty": 1}, {"name": "Latte", "qty": 1}]', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days');

-- Order Items hace 5 días
INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase, created_at, updated_at) VALUES
('80000000-0000-0000-0000-000000000011', '70000000-0000-0000-0000-000000000007', '60000000-0000-0000-0000-000000000001', 2, 65.00, NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'), -- Caramel Frappé x2
('80000000-0000-0000-0000-000000000012', '70000000-0000-0000-0000-000000000007', '60000000-0000-0000-0000-000000000014', 1, 38.00, NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'), -- Muffin
('80000000-0000-0000-0000-000000000013', '70000000-0000-0000-0000-000000000008', '60000000-0000-0000-0000-000000000007', 1, 48.00, NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'), -- Cappuccino
('80000000-0000-0000-0000-000000000014', '70000000-0000-0000-0000-000000000008', '60000000-0000-0000-0000-000000000006', 1, 45.00, NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'); -- Latte

-- Órdenes hace 6 días (25 Oct 2025)
INSERT INTO orders (order_id, user_id, order_date, status, total_amount, points_earned, payment_type, items_summary_json, created_at, updated_at) VALUES
('70000000-0000-0000-0000-000000000009', '10000000-0000-0000-0000-000000000005', NOW() - INTERVAL '6 days', 'paid', 143.00, 14.30, 'card', '[{"name": "Mocha Frappé", "qty": 1}, {"name": "Croissant", "qty": 2}]', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days');

-- Order Items hace 6 días
INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase, created_at, updated_at) VALUES
('80000000-0000-0000-0000-000000000015', '70000000-0000-0000-0000-000000000009', '60000000-0000-0000-0000-000000000002', 1, 70.00, NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days'), -- Mocha Frappé
('80000000-0000-0000-0000-000000000016', '70000000-0000-0000-0000-000000000009', '60000000-0000-0000-0000-000000000012', 2, 35.00, NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days'); -- Croissant x2

-- Órdenes de HOY (para tener datos frescos)
INSERT INTO orders (order_id, user_id, order_date, status, total_amount, points_earned, payment_type, items_summary_json, created_at, updated_at) VALUES
('70000000-0000-0000-0000-000000000010', '10000000-0000-0000-0000-000000000003', NOW() - INTERVAL '3 hours', 'paid', 203.00, 20.30, 'card', '[{"name": "Caramel Frappé", "qty": 1}, {"name": "Latte", "qty": 2}, {"name": "Cookie", "qty": 1}]', NOW() - INTERVAL '3 hours', NOW() - INTERVAL '3 hours'),
('70000000-0000-0000-0000-000000000011', '10000000-0000-0000-0000-000000000004', NOW() - INTERVAL '1 hour', 'paid', 118.00, 11.80, 'cash', '[{"name": "Cappuccino", "qty": 1}, {"name": "Mocha Frappé", "qty": 1}]', NOW() - INTERVAL '1 hour', NOW() - INTERVAL '1 hour');

-- Order Items de HOY
INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase, created_at, updated_at) VALUES
('80000000-0000-0000-0000-000000000017', '70000000-0000-0000-0000-000000000010', '60000000-0000-0000-0000-000000000001', 1, 65.00, NOW() - INTERVAL '3 hours', NOW() - INTERVAL '3 hours'), -- Caramel Frappé
('80000000-0000-0000-0000-000000000018', '70000000-0000-0000-0000-000000000010', '60000000-0000-0000-0000-000000000006', 2, 45.00, NOW() - INTERVAL '3 hours', NOW() - INTERVAL '3 hours'), -- Latte x2
('80000000-0000-0000-0000-000000000019', '70000000-0000-0000-0000-000000000010', '60000000-0000-0000-0000-000000000015', 1, 32.00, NOW() - INTERVAL '3 hours', NOW() - INTERVAL '3 hours'), -- Cookie
('80000000-0000-0000-0000-000000000020', '70000000-0000-0000-0000-000000000011', '60000000-0000-0000-0000-000000000007', 1, 48.00, NOW() - INTERVAL '1 hour', NOW() - INTERVAL '1 hour'), -- Cappuccino
('80000000-0000-0000-0000-000000000021', '70000000-0000-0000-0000-000000000011', '60000000-0000-0000-0000-000000000002', 1, 70.00, NOW() - INTERVAL '1 hour', NOW() - INTERVAL '1 hour'); -- Mocha Frappé

-- =============================================
-- 5. FAVORITOS DE USUARIOS
-- =============================================

-- Favoritos de Armando (user_id: ...003)
INSERT INTO user_favorites (user_id, product_id) VALUES
('10000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000001'), -- Caramel Frappé
('10000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000002'), -- Mocha Frappé
('10000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000006'), -- Latte
('10000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000012'), -- Croissant
('10000000-0000-0000-0000-000000000003', '60000000-0000-0000-0000-000000000018'); -- Iced Coffee

-- Favoritos de Brenda (user_id: ...004)
INSERT INTO user_favorites (user_id, product_id) VALUES
('10000000-0000-0000-0000-000000000004', '60000000-0000-0000-0000-000000000007'), -- Cappuccino
('10000000-0000-0000-0000-000000000004', '60000000-0000-0000-0000-000000000013'), -- Panqué
('10000000-0000-0000-0000-000000000004', '60000000-0000-0000-0000-000000000010'), -- Flat White
('10000000-0000-0000-0000-000000000004', '60000000-0000-0000-0000-000000000014'); -- Muffin

-- Favoritos de Carlos (user_id: ...005)
INSERT INTO user_favorites (user_id, product_id) VALUES
('10000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000008'), -- Americano
('10000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000009'), -- Espresso
('10000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000019'), -- Cold Brew
('10000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000015'), -- Cookie
('10000000-0000-0000-0000-000000000005', '60000000-0000-0000-0000-000000000003'); -- Vanilla Frappé

--INSERT DE RODRIGO DESPLIEGUE


INSERT INTO public.promotions
    (promotion_id, code, discount_type, discount_value, start_date, end_date, created_at, updated_at)
VALUES
    ('a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d', 'PROMO20', 'percentage', 20.0, '2025-01-01 00:00:00', '2025-01-31 23:59:59', '2025-01-01 10:00:00', '2025-01-01 10:00:00');
INSERT INTO public.promotions
    (promotion_id, code, discount_type, discount_value, start_date, end_date, created_at, updated_at)
VALUES
    ('b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e', 'DIEZMXN', 'fixed_amount', 10.00, '2026-02-01 00:00:00', '2026-02-14 23:59:59', '2025-11-01 14:30:00', '2025-11-01 14:30:00');
INSERT INTO public.promotions
    (promotion_id, code, discount_type, discount_value, start_date, end_date, created_at, updated_at)
VALUES
    ('f0a1b2c3-d4e5-4f6a-7b8c-9d0e1f2a3b4c', 'NAVIDAD25', 'percentage', 25.0, '2025-12-01 00:00:00', '2025-12-01 23:59:59', '2025-11-15 09:00:00', '2025-11-15 09:00:00');
INSERT INTO public.promotions
    (promotion_id, code, discount_type, discount_value, start_date, end_date, created_at, updated_at)
VALUES
    ('e1b2c3d4-a5f6-4a7b-8c9d-0e1f2a3b4c5d', 'QUINCEFIJO', 'fixed_amount', 15.00, '2026-03-20 00:00:00', '2026-03-31 23:59:59', '2026-03-01 12:00:00', '2026-03-01 12:00:00');
INSERT INTO public.promotions
    (promotion_id, code, discount_type, discount_value, start_date, end_date, created_at, updated_at)
VALUES
    ('c2d3e4f5-b6a7-4b8c-9d0e-1f2a3b4c5d6e', 'JUNIO10', 'percentage', 10.0, '2024-06-10 00:00:00', '2024-06-17 23:59:59', '2024-06-01 08:00:00', '2024-06-01 08:00:00');
-- Promoción faltante para evitar error de FK en product_promotions
INSERT INTO public.promotions
    (promotion_id, code, discount_type, discount_value, start_date, end_date, created_at, updated_at)
VALUES
    ('5e7e9ddb-6323-4acf-a80b-17216f5cc63d', 'BIENVENIDA', 'percentage', 15.0, '2025-11-01 00:00:00', '2025-11-30 23:59:59', '2025-11-01 10:00:00', '2025-11-01 10:00:00');

INSERT INTO public.product_promotions
(product_id, promotion_id, created_at, updated_at)
VALUES
(
    '60000000-0000-0000-0000-000000000005',
    'c2d3e4f5-b6a7-4b8c-9d0e-1f2a3b4c5d6e', 
    NOW(),
    NOW()
);

INSERT INTO public.product_promotions
(product_id, promotion_id, created_at, updated_at)
VALUES
(
    '60000000-0000-0000-0000-000000000006',
    'b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e', 
    NOW(),
    NOW()
);

INSERT INTO public.product_promotions
(product_id, promotion_id, created_at, updated_at)
VALUES
(
    '60000000-0000-0000-0000-000000000007',
    '5e7e9ddb-6323-4acf-a80b-17216f5cc63d', 
    NOW(),
    NOW()
);
INSERT INTO public.product_promotions
(product_id, promotion_id, created_at, updated_at)
VALUES
(
    '60000000-0000-0000-0000-000000000008',
    'f0a1b2c3-d4e5-4f6a-7b8c-9d0e1f2a3b4c', 
    NOW(),
    NOW()
);

INSERT INTO public.product_promotions
(product_id, promotion_id, created_at, updated_at)
VALUES
(
    '60000000-0000-0000-0000-000000000009',
    'e1b2c3d4-a5f6-4a7b-8c9d-0e1f2a3b4c5d', 
    NOW(),
    NOW()
);

INSERT INTO public.product_promotions
(product_id, promotion_id, created_at, updated_at)
VALUES
(
    '60000000-0000-0000-0000-000000000010',
    'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d', 
    NOW(),
    NOW()
);

INSERT INTO public.product_promotions
(product_id, promotion_id, created_at, updated_at)
VALUES
(
    '60000000-0000-0000-0000-000000000011',
    'c2d3e4f5-b6a7-4b8c-9d0e-1f2a3b4c5d6e', 
    NOW(),
    NOW()
);

INSERT INTO public.product_promotions
(product_id, promotion_id, created_at, updated_at)
VALUES
(
    '60000000-0000-0000-0000-000000000012',
    'b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e', 
    NOW(),
    NOW()
);