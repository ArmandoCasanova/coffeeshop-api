

-- 1. USUARIOS
INSERT INTO users (user_id, role, name, last_name, email, password, points, is_verified, birth_date, created_at, updated_at) VALUES
('10000000-0000-0000-0000-000000000001', 'admin', 'Alex', 'Admin', 'admin@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 0.00, TRUE, '1985-05-15', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('10000000-0000-0000-0000-000000000002', 'staff', 'Sara', 'Staff', 'staff@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 0.00, TRUE, '1992-11-20', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('10000000-0000-0000-0000-000000000003', 'customer', 'Armando', 'Casanova', 'armando@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 50.00, TRUE, '1995-03-10', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('10000000-0000-0000-0000-000000000004', 'customer', 'Brenda', 'Cliente', 'brenda@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 15.00, TRUE, '1998-07-25', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('10000000-0000-0000-0000-000000000005', 'customer', 'Carlos', 'Cliente', 'carlos@cafe.com', '$2b$12$kBBV85vGJA5NdKYyJCxPveKABTSO5aNjdKq49RpVxvJATAmHy7v6m', 0.00, TRUE, '2000-12-01', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00');

-- 2. INGREDIENTES (INVENTARIO)
INSERT INTO ingredients (ingredient_id, name, unit_of_measure, stock_current_level, stock_optimal_level, created_at, updated_at) VALUES
('20000000-0000-0000-0000-000000000001', 'Agua Filtrada', 'ml', 50000, 30000, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000002', 'Leche Entera Base', 'ml', 15000, 10000, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000003', 'Leche de Almendras', 'ml', 8000, 5000, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000004', 'Café Espresso Regular', 'shot', 200, 150, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000009', 'Café Espresso Descafeinado', 'shot', 100, 50, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000005', 'Base Frappe Vainilla', 'g', 5000, 3000, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000006', 'Jarabe Chocolate', 'ml', 3000, 2000, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000007', 'Crema Batida', 'g', 1000, 500, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000008', 'Panqué Base', 'g', 20, 15, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000010', 'Té Negro Granel', 'g', 100, 50, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('20000000-0000-0000-0000-000000000011', 'Leche Deslactosada', 'ml', 5000, 3000, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00');

-- 3. GRUPOS DE PERSONALIZACIÓN
INSERT INTO customization_groups (group_id, system_name, display_name, created_at, updated_at) VALUES
('30000000-0000-0000-0000-000000000001', 'Tamaño Frappe', 'Tamaño', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('30000000-0000-0000-0000-000000000002', 'Tipo de Leche Frappe', 'Tipo de Leche', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('30000000-0000-0000-0000-000000000003', 'Extra Frappe', 'Extra', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('30000000-0000-0000-0000-000000000004', 'Tipo de Café Frappe', 'Tipo de Café', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('30000000-0000-0000-0000-000000000005', 'Endulzante Frappe', 'Endulzante', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00');

-- 4. OPCIONES DE PERSONALIZACIÓN
INSERT INTO customization_options (option_id, group_id, name, extra_cost, is_size_option, consumed_ingredient_id, quantity_consumed, details, created_at, updated_at) VALUES
-- GRUPO TAMAÑO
('40000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', 'Chico', 0.00, TRUE, NULL, 0.00, '160ml (Base)', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('40000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001', 'Mediano', 5.00, TRUE, '20000000-0000-0000-0000-000000000002', 90.00, '250ml - Leche Extra', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), -- +90ml
('40000000-0000-0000-0000-000000000003', '30000000-0000-0000-0000-000000000001', 'Venti', 10.00, TRUE, '20000000-0000-0000-0000-000000000002', 150.00, '310ml - Leche Extra', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), -- +150ml

-- GRUPO LECHE
('40000000-0000-0000-0000-000000000004', '30000000-0000-0000-0000-000000000002', 'Leche Entera (Base)', 0.00, FALSE, '20000000-0000-0000-0000-000000000002', 0.00, '', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), 
('40000000-0000-0000-0000-000000000005', '30000000-0000-0000-0000-000000000002', 'Leche de Almendras', 12.00, FALSE, '20000000-0000-0000-0000-000000000003', 0.00, '', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), 
('40000000-0000-0000-0000-000000000006', '30000000-0000-0000-0000-000000000002', 'Deslactosada', 8.00, FALSE, '20000000-0000-0000-0000-000000000011', 0.00, '', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),

-- GRUPO CAFÉ
('40000000-0000-0000-0000-000000000008', '30000000-0000-0000-0000-000000000004', 'Regular (Base)', 0.00, FALSE, '20000000-0000-0000-0000-000000000004', 0.00, '', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('40000000-0000-0000-0000-000000000009', '30000000-0000-0000-0000-000000000004', 'Descafeinado', 0.00, FALSE, '20000000-0000-0000-0000-000000000009', 0.00, '', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),

-- GRUPO EXTRA
('40000000-0000-0000-0000-000000000007', '30000000-0000-0000-0000-000000000003', 'Extra Crema Batida', 15.00, FALSE, '20000000-0000-0000-0000-000000000007', 50.00, 'Añade 50g de crema', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00');

-- 5. CATEGORÍAS
INSERT INTO product_categories (category_id, name, description, created_at, updated_at) VALUES
('50000000-0000-0000-0000-000000000001', 'Frappés', 'Bebidas frías mezcladas con hielo.', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('50000000-0000-0000-0000-000000000002', 'Bebidas Calientes', 'Cafés y chocolates calientes.', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('50000000-0000-0000-0000-000000000003', 'Panadería', 'Postres y bocadillos.', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('50000000-0000-0000-0000-000000000004', 'Té y Tisanas', 'Infusiones naturales.', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('50000000-0000-0000-0000-000000000005', 'Bebidas Frías', 'Bebidas no mezcladas con hielo.', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00');

-- 6. PRODUCTOS
INSERT INTO products (product_id, name, base_price, image_url, is_available, category_info_json, customization_details_json, created_at, updated_at) VALUES
('60000000-0000-0000-0000-000000000001', 'Latte (Chico)', 35.00, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8LwumF4lCEmajcOOE7VtT23bJY7qgd4LQgg&s', TRUE, '[{"id": "50000000-0000-0000-0000-000000000002", "name": "Bebidas Calientes"}]', '{"groups": ["Tamaño", "Tipo de Leche", "Tipo de Café"]}', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('60000000-0000-0000-0000-000000000002', 'Frappé Mocha (Chico)', 60.00, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8LwumF4lCEmajcOOE7VtT23bJY7qgd4LQgg&s', TRUE, '[{"id": "50000000-0000-0000-0000-000000000001", "name": "Frappés"}]', '{"groups": ["Tamaño", "Extra"]}', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('60000000-0000-0000-0000-000000000003', 'Panqué de Plátano', 45.00, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8LwumF4lCEmajcOOE7VtT23bJY7qgd4LQgg&s', TRUE, '[{"id": "50000000-0000-0000-0000-000000000003", "name": "Panadería"}]', '[]', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('60000000-0000-0000-0000-000000000004', 'Americano (Chico)', 30.00, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8LwumF4lCEmajcOOE7VtT23bJY7qgd4LQgg&s', TRUE, '[{"id": "50000000-0000-0000-0000-000000000002", "name": "Bebidas Calientes"}]', '{"groups": ["Tamaño", "Tipo de Café"]}', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('60000000-0000-0000-0000-000000000005', 'Té Negro (Chico)', 25.00, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8LwumF4lCEmajcOOE7VtT23bJY7qgd4LQgg&s', TRUE, '[{"id": "50000000-0000-0000-0000-000000000004", "name": "Té y Tisanas"}]', '{"groups": ["Tamaño"]}', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'),
('60000000-0000-0000-0000-000000000010', 'Capuchino (Chico)', 40.00, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8LwumF4lCEmajcOOE7VtT23bJY7qgd4LQgg&s', TRUE, '[{"id": "50000000-0000-0000-0000-000000000002", "name": "Bebidas Calientes"}]', '{"groups": ["Tamaño", "Tipo de Leche"]}', '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00');

-- 7. RECETA BASE (product_ingredients) - **INCLUYE AUDITORÍA**
INSERT INTO product_ingredients (product_id, ingredient_id, quantity_required, created_at, updated_at) VALUES
('60000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000004', 1.0, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), -- Latte (Chico) - 1 shot regular
('60000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000002', 160.0, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), -- Latte (Chico) - 160ml Leche Entera
('60000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000005', 100.0, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), -- Frappé Mocha (Chico) - 100g Base Frappe
('60000000-0000-0000-0000-000000000004', '20000000-0000-0000-0000-000000000004', 2.0, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), -- Americano (Chico) - 2 shots regular
('60000000-0000-0000-0000-000000000004', '20000000-0000-0000-0000-000000000001', 100.0, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00'), -- Americano (Chico) - 100ml Agua
('60000000-0000-0000-0000-000000000003', '20000000-0000-0000-0000-000000000008', 1.0, '2024-01-01 10:00:00+00', '2024-01-01 10:00:00+00');  -- Panqué - 1 unidad

-- 8. VINCULACIÓN DE PERSONALIZACIÓN A PRODUCTOS (product_customization_groups) - M:M
INSERT INTO product_customization_groups (product_id, group_id) VALUES
('60000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001'), -- Latte: Tamaño
('60000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000002'), -- Latte: Tipo de Leche
('60000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001'); -- Frappé Mocha: Tamaño

-- 9. VINCULACIÓN DE CATEGORÍAS (product_category_link) - M:M
INSERT INTO product_category_link (product_id, category_id) VALUES
('60000000-0000-0000-0000-000000000001', '50000000-0000-0000-0000-000000000002'), -- Latte -> Bebidas Calientes
('60000000-0000-0000-0000-000000000002', '50000000-0000-0000-0000-000000000001'), -- Frappé Mocha -> Frappés
('60000000-0000-0000-0000-000000000003', '50000000-0000-0000-0000-000000000003'); -- Panqué -> Panadería

-- 10. ORDEN PRINCIPAL (paid, card) - Incluye Auditoría
INSERT INTO orders (order_id, user_id, order_date, status, total_amount, points_earned, payment_type, items_summary_json, created_at, updated_at) VALUES
('70000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000003', '2025-10-10 10:30:00+00', 'paid', 100.00, 10.00, 'card', '[{"name": "Frappé Mocha Venti", "qty": 1, "custom": "Almendras, Crema Extra"}]', '2025-10-10 10:30:00+00', '2025-10-10 10:30:00+00');

-- Items de la Orden Principal - Incluye Auditoría
INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase, created_at, updated_at) VALUES
('80000000-0000-0000-0000-000000000001', '70000000-0000-0000-0000-000000000001', '60000000-0000-0000-0000-000000000002', 1, 85.00, '2025-10-10 10:30:00+00', '2025-10-10 10:30:00+00'); -- Frappé

-- Personalización del Frappé - M:M
INSERT INTO order_item_customization (order_item_id, option_id, extra_cost_at_purchase) VALUES
('80000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000003', 10.00), -- Venti (+150ml)
('80000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000005', 12.00), -- Leche Almendras
('80000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000007', 15.00); -- Extra Crema Batida

-- Transacción Principal - Incluye Auditoría
INSERT INTO transactions (transaction_id, order_id, amount, status, transaction_date) VALUES
('90000000-0000-0000-0000-000000000001', '70000000-0000-0000-0000-000000000001', 100.00, 'success', '2025-10-10 10:31:00+00');
