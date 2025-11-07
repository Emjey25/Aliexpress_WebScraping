# 🛒 AliExpress Web Scraper & Database Management System

Sistema completo de **web scraping** para monitorear la competencia en AliExpress y gestionar un catálogo de productos con análisis de precios, inventario y rentabilidad.

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Base de Datos](#-base-de-datos)
- [Código Python](#-código-python)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Consultas Útiles](#-consultas-útiles)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Consideraciones de Seguridad](#-consideraciones-de-seguridad)

---

## 🎯 Descripción del Proyecto

Este proyecto permite a vendedores de AliExpress:

- **Automatizar** la recopilación de datos de productos de la competencia
- **Monitorear** precios, valoraciones, reseñas y stock disponible
- **Gestionar** inventario propio y análisis de rentabilidad
- **Comparar** precios con la competencia
- **Generar alertas** sobre cambios importantes en el mercado

---

## 📁 Estructura del Proyecto

```
PythonWebScraping/
│
├── example2.py                      # Script principal del scraper
├── example.py                       # Script de prueba de conexión
│
├── ScriptDB_Aliexpress.sql         # Dump completo de la BD (estructura + datos)
├── InsertarDatosBD_Aliexpress.sql  # INSERTs de datos de ejemplo
├── ConsultasBD_Aliexpress.sql      # Consultas SQL útiles para análisis
│
└── README.md                        # Documentación (este archivo)
```

---

## 🗄️ Base de Datos

### Diagrama de Relaciones

La base de datos `aliexpress_vendedor` está diseñada con las siguientes tablas:

#### **Tabla: `Producto`**

Catálogo de productos propios del vendedor.

| Campo                 | Tipo          | Descripción                        |
| --------------------- | ------------- | ---------------------------------- |
| `product_id`          | INT (PK)      | Identificador único del producto   |
| `sku`                 | VARCHAR(50)   | Código único del producto (UNIQUE) |
| `nombre`              | VARCHAR(255)  | Nombre del producto                |
| `descripcion`         | TEXT          | Descripción detallada              |
| `categoria`           | VARCHAR(100)  | Categoría del producto             |
| `precio_actual`       | DECIMAL(10,2) | Precio de venta actual             |
| `costo_proveedor`     | DECIMAL(10,2) | Costo de compra al proveedor       |
| `comision_aliexpress` | DECIMAL(5,2)  | % de comisión de AliExpress        |
| `fecha_creacion`      | TIMESTAMP     | Fecha de creación del registro     |

#### **Tabla: `Datos_Competencia`** ⭐ (Principal para scraping)

Almacena información de productos competidores extraída mediante web scraping.

| Campo                | Tipo          | Descripción                        |
| -------------------- | ------------- | ---------------------------------- |
| `competencia_id`     | INT (PK)      | ID único del registro              |
| `product_id`         | INT (FK)      | Referencia al producto propio      |
| `nombre_competidor`  | VARCHAR(255)  | Nombre del vendedor competidor     |
| `precio_competencia` | DECIMAL(10,2) | Precio del competidor              |
| `stock_visible`      | TINYINT(1)    | Stock visible (1=disponible, 0=no) |
| `valoracion`         | DECIMAL(3,2)  | Valoración promedio (1-5)          |
| `numero_resenas`     | INT           | Número de reseñas                  |
| `url`                | VARCHAR(500)  | URL del producto competidor        |
| `fecha_scraping`     | TIMESTAMP     | Fecha y hora del scraping          |

#### **Tabla: `Inventario`**

Control de stock de productos propios.

| Campo                 | Tipo      | Descripción                         |
| --------------------- | --------- | ----------------------------------- |
| `inventario_id`       | INT (PK)  | ID único                            |
| `product_id`          | INT (FK)  | Referencia al producto              |
| `stock_actual`        | INT       | Cantidad disponible actualmente     |
| `stock_minimo`        | INT       | Stock mínimo antes de reordenar     |
| `stock_maximo`        | INT       | Stock máximo permitido              |
| `fecha_actualizacion` | TIMESTAMP | Última actualización del inventario |

#### **Tabla: `Venta`**

Registro histórico de ventas.

| Campo             | Tipo          | Descripción             |
| ----------------- | ------------- | ----------------------- |
| `venta_id`        | INT (PK)      | ID único de la venta    |
| `product_id`      | INT (FK)      | Producto vendido        |
| `cantidad`        | INT           | Unidades vendidas       |
| `precio_unitario` | DECIMAL(10,2) | Precio por unidad       |
| `precio_total`    | DECIMAL(10,2) | Total de la venta       |
| `fecha_venta`     | TIMESTAMP     | Fecha de la transacción |

#### **Otras Tablas**

- **`Proveedor`**: Información de proveedores
- **`Producto_Proveedor`**: Relación muchos a muchos entre productos y proveedores
- **`Valoracion`**: Reseñas de clientes sobre productos propios
- **`Alerta`**: Sistema de notificaciones automáticas

### Relaciones Clave

- `Producto` → `Datos_Competencia` (1:N)
- `Producto` → `Inventario` (1:1)
- `Producto` → `Venta` (1:N)
- `Producto` → `Valoracion` (1:N)

---

## 🐍 Código Python

### Clase Principal: `AliExpressScraper`

#### **Constructor**

```python
def __init__(self, db_host, db_user, db_password, db_name):
```

Inicializa la conexión a MySQL y configura headers para las peticiones HTTP.

**Parámetros:**

- `db_host`: Servidor MySQL (ej: "localhost")
- `db_user`: Usuario de MySQL (ej: "root")
- `db_password`: Contraseña de MySQL
- `db_name`: Nombre de la base de datos (ej: "aliexpress_vendedor")

#### **Método: `extraer_producto(url)`**

```python
def extraer_producto(self, url):
```

Extrae información de un producto de AliExpress mediante web scraping.

**Retorna un diccionario con:**

- `nombre`: Nombre del producto
- `precio`: Precio en formato decimal
- `valoracion`: Calificación promedio
- `numero_resenas`: Cantidad de reseñas
- `stock_visible`: Disponibilidad de stock
- `url`: URL original

**Manejo de errores:**

- Utiliza `try/except` para capturar errores HTTP
- Logging de errores con `logger.error()`
- Retorna `None` si falla la extracción

#### **Método: `insertar_en_bd(producto, product_id)`**

```python
def insertar_en_bd(self, producto, product_id):
```

Inserta los datos extraídos en la tabla `Datos_Competencia`.

**Parámetros:**

- `producto`: Diccionario con datos del producto
- `product_id`: ID del producto propio con el que se relaciona

**Query SQL:**

```sql
INSERT INTO Datos_Competencia
(product_id, nombre_competidor, precio_competencia,
 stock_visible, valoracion, numero_resenas, url)
VALUES (%s, %s, %s, %s, %s, %s, %s)
```

#### **Método: `ejecutar_scraping(urls)`**

```python
def ejecutar_scraping(self, urls):
```

Itera sobre una lista de URLs y ejecuta el scraping con intervalo de 3 segundos entre peticiones (para evitar bloqueos).

### Flujo de Ejecución

```
┌─────────────────┐
│  Inicializar    │
│    Scraper      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Conectar a BD  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Iterar URLs   │◄──────┐
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│ HTTP Request    │       │
│ (BeautifulSoup) │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  Parsear HTML   │       │
│  Extraer Datos  │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│   INSERT BD     │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  Sleep 3 seg    │───────┘
└─────────────────┘
```

---

## 🚀 Instalación

### 1. **Requisitos Previos**

- Python 3.7+
- MySQL 8.0+
- pip (gestor de paquetes de Python)

### 2. **Clonar el Repositorio**

```bash
git clone https://github.com/Emjey25/JavandoCodigo.git
cd PythonWebScraping
```

### 3. **Instalar Dependencias Python**

```powershell
pip install requests beautifulsoup4 mysql-connector-python
```

**Dependencias:**

- `requests`: Para hacer peticiones HTTP
- `beautifulsoup4`: Para parsear HTML
- `mysql-connector-python`: Conector MySQL

### 4. **Configurar Base de Datos**

#### Opción A: Importar dump completo

```bash
mysql -u root -p < ScriptDB_Aliexpress.sql
```

#### Opción B: Crear manualmente

```bash
# 1. Crear la base de datos
mysql -u root -p -e "CREATE DATABASE aliexpress_vendedor;"

# 2. Importar estructura
mysql -u root -p aliexpress_vendedor < ScriptDB_Aliexpress.sql

# 3. Insertar datos de ejemplo (opcional)
mysql -u root -p aliexpress_vendedor < InsertarDatosBD_Aliexpress.sql
```

### 5. **Configurar Credenciales**

⚠️ **IMPORTANTE**: Edita `example2.py` y reemplaza las credenciales:

```python
scraper = AliExpressScraper(
    'localhost',           # db_host
    'root',                # db_user
    'TU_CONTRASEÑA_AQUI', # db_password (NO dejar en el código)
    'aliexpress_vendedor'  # db_name
)
```

**Recomendación de seguridad**: Usa variables de entorno:

```python
import os
password = os.getenv('MYSQL_PASSWORD')
```

---

## 💻 Uso

### Ejecución Básica

```powershell
python example2.py
```

### Personalizar URLs

Edita la lista de URLs en `example2.py`:

```python
urls = [
    'https://es.aliexpress.com/item/1005007813235975.html',
    'https://es.aliexpress.com/item/OTRO_PRODUCTO.html',
    # Agrega más URLs aquí
]
```

### Ajustar Product ID

El scraper asocia cada producto competidor a un `product_id` de tu catálogo. Modifica según corresponda:

```python
# En el método ejecutar_scraping:
self.insertar_en_bd(producto, 1)  # Cambiar '1' por el ID real
```

### Salida Esperada

```
INFO:__main__:Scrapeando: https://es.aliexpress.com/item/...
INFO:__main__:Extraído: Protector Pantalla Vidrio Templado
INFO:__main__:Insertado en BD
```

---

## 📊 Consultas Útiles

### 1. Productos con Stock Bajo

```sql
SELECT p.nombre, i.stock_actual, i.stock_minimo
FROM Producto p
JOIN Inventario i ON p.product_id = i.product_id
WHERE i.stock_actual < i.stock_minimo;
```

### 2. Productos Más Vendidos (últimos 30 días)

```sql
SELECT p.nombre, SUM(v.cantidad) as total
FROM Producto p
JOIN Venta v ON p.product_id = v.product_id
WHERE v.fecha_venta >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY p.product_id
ORDER BY total DESC;
```

### 3. Comparación de Precios con Competencia

```sql
SELECT
    p.nombre,
    p.precio_actual,
    dc.precio_competencia,
    ROUND(((p.precio_actual - dc.precio_competencia) / dc.precio_competencia * 100), 2)
        as diferencia_porcentual
FROM Producto p
JOIN Datos_Competencia dc ON p.product_id = dc.product_id;
```

### 4. Análisis de Rentabilidad

```sql
SELECT
    p.nombre,
    p.precio_actual,
    p.costo_proveedor,
    (p.precio_actual - p.costo_proveedor -
     (p.precio_actual * p.comision_aliexpress / 100)) as margen
FROM Producto p
ORDER BY margen DESC;
```

### 5. Historial de Precios de Competencia

```sql
SELECT
    dc.nombre_competidor,
    dc.precio_competencia,
    dc.fecha_scraping
FROM Datos_Competencia dc
WHERE dc.product_id = 1
ORDER BY dc.fecha_scraping DESC
LIMIT 10;
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología      | Versión | Propósito                |
| --------------- | ------- | ------------------------ |
| Python          | 3.7+    | Lenguaje principal       |
| MySQL           | 8.0+    | Base de datos relacional |
| BeautifulSoup4  | 4.x     | Parseo de HTML           |
| Requests        | 2.x     | Peticiones HTTP          |
| mysql-connector | 8.x     | Conector Python-MySQL    |
| Git             | 2.x     | Control de versiones     |

---

## 🔒 Consideraciones de Seguridad

### 1. **Credenciales**

❌ **NO** guardes contraseñas en el código
✅ Usa variables de entorno o archivos `.env`

```python
# Crear archivo .env:
# MYSQL_PASSWORD=tu_contraseña

import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv('MYSQL_PASSWORD')
```

### 2. **Web Scraping Responsable**

- ⏱️ Respetar intervalos de tiempo entre peticiones (actualmente 3 segundos)
- 🤖 Identificarte con User-Agent apropiado
- 📜 Revisar los Términos de Servicio de AliExpress
- 🚫 No sobrecargar servidores con peticiones masivas

### 3. **Manejo de Errores**

El código incluye logging de errores pero considera:

- Implementar reintentos con exponential backoff
- Guardar logs en archivos para auditoría
- Monitorear cambios en la estructura HTML de AliExpress

### 4. **Inyección SQL**

✅ El código usa consultas parametrizadas (`%s`) lo cual previene inyección SQL:

```python
cursor.execute(query, datos)  # ✅ Correcto
# cursor.execute(f"INSERT... {variable}")  # ❌ NUNCA hacer esto
```

---

## 📝 Notas Adicionales

### Limitaciones Actuales

- **JavaScript**: BeautifulSoup solo parsea HTML estático. Si AliExpress carga datos con JavaScript, considera usar:

  - Selenium
  - Playwright
  - Puppeteer
  - API pública (si existe)

- **Selectores**: Los selectores CSS pueden cambiar. El código usa clases genéricas como fallback.

- **Captchas**: AliExpress puede bloquear scraping con captchas. Soluciones:
  - Proxies rotatorios
  - Servicios de resolución de captchas
  - Reducir frecuencia de peticiones

### Mejoras Futuras

- [ ] Implementar scraping asíncrono (aiohttp)
- [ ] Dashboard web con Flask/Django
- [ ] Notificaciones automáticas por email
- [ ] Soporte para múltiples marketplaces
- [ ] Sistema de caché para URLs ya scrapeadas
- [ ] Tests unitarios con pytest
- [ ] Dockerización del proyecto

---

## 👨‍💻 Autor

**Emjey25**  
GitHub: [@Emjey25](https://github.com/Emjey25)

---

## 📄 Licencia

Este proyecto es de código abierto. Úsalo bajo tu propia responsabilidad y respeta las políticas de web scraping de los sitios objetivo.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras bugs o tienes mejoras:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

## ⚠️ Disclaimer

Este proyecto es **solo con fines educativos**. El web scraping puede violar los Términos de Servicio de algunos sitios web. Úsalo de manera responsable y ética. El autor no se hace responsable del uso indebido de este código.

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0.0
