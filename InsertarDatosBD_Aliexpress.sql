INSERT INTO Producto (sku, nombre, categoria, precio_actual, costo_proveedor, comision_aliexpress) VALUES
('AX-TECH-001', 'Protector Pantalla Vidrio Templado', 'Tecnología', 5.99, 1.20, 15),
('AX-TECH-002', 'Cable USB Carga Rápida', 'Tecnología', 7.99, 2.00, 15),
('AX-MODA-001', 'Sudadera Hoodie', 'Moda', 19.99, 8.50, 15);

INSERT INTO Inventario (product_id, stock_actual, stock_minimo) VALUES (1, 45, 10), (2, 8, 15), (3, 22, 10);

INSERT INTO Venta (product_id, cantidad, precio_unitario, precio_total) VALUES (1, 5, 5.99, 29.95), (2, 2, 7.99, 15.98), (3, 1, 19.99, 19.99);

INSERT INTO Valoracion (product_id, calificacion, comentario) VALUES (1, 5, 'Excelente'), (2, 4, 'Bueno'), (3, 3, 'Regular');

INSERT INTO Proveedor (nombre, email, tiempo_entrega) VALUES ('Tech Supplies', 'contact@tech.com', 12), ('Fashion Direct', 'info@fashion.com', 18);

INSERT INTO Datos_Competencia (product_id, nombre_competidor, precio_competencia, stock_visible, valoracion, numero_resenas) VALUES (1, 'Vendedor X', 5.49, true, 4.7, 234), (2, 'Tech Store', 8.99, true, 4.5, 156);
