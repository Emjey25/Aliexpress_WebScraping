import mysql.connector

# Datos de conexión
mi_conexion = mysql.connector.connect(
    host="localhost",       # IP de tu servidor MySQL (usualmente localhost)
    user="root",            # Usuario de MySQL (por defecto muchas veces es root)
    password="250504",# Cambia esto por tu contraseña
    database="aliexpress_vendedor"    # Nombre de la base de datos que creaste
)

# Crear cursor y ejecutar consulta simple
cursor = mi_conexion.cursor()
cursor.execute("SHOW TABLES")
print("Tablas en la base de datos:")
for tabla in cursor:
    print(tabla)

# Cierra la conexión correctamente
cursor.close()
mi_conexion.close()
