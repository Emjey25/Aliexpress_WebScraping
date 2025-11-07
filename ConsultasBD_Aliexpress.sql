

/* Productos bajo stock*/
SELECT p.nombre, i.stock_actual, i.stock_minimo FROM Producto p JOIN Inventario i ON p.product_id = i.product_id WHERE i.stock_actual < i.stock_minimo;

/* Productos más vendidos*/
SELECT p.nombre, SUM(v.cantidad) as total FROM Producto p JOIN Venta v ON p.product_id = v.product_id WHERE v.fecha_venta >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) GROUP BY p.product_id ORDER BY total DESC;

/* Comparación de precios*/
SELECT p.nombre, p.precio_actual, dc.precio_competencia, ROUND(((p.precio_actual - dc.precio_competencia) / dc.precio_competencia * 100), 2) as diferencia_porcentual FROM Producto p JOIN Datos_Competencia dc ON p.product_id = dc.product_id;

/*Rentabilidad por producto*/
SELECT p.nombre, p.precio_actual, p.costo_proveedor, (p.precio_actual - p.costo_proveedor - (p.precio_actual * p.comision_aliexpress / 100)) as margen FROM Producto p ORDER BY margen DESC;

