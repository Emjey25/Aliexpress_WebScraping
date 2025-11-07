import requests
from bs4 import BeautifulSoup
import mysql.connector
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AliExpressScraper:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.base_url = "https://www.aliexpress.com"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.conexion = mysql.connector.connect(
            host="localhost",       # IP de tu servidor MySQL (usualmente localhost)
            user="root",            # Usuario de MySQL (por defecto muchas veces es root)
            password="250504", # Cambia esto por tu contraseña
            database="aliexpress_vendedor"    # Nombre de la base de datos que creaste
        )
        
    def extraer_producto(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            producto = {
                'nombre': soup.find('h1').text.strip() if soup.find('h1') else "N/A",
                'precio': float(soup.find('span', {'class': 'price'}).text.strip().replace('$', '')) if soup.find('span', {'class': 'price'}) else 0,
                'valoracion': float(soup.find('span', {'class': 'rating'}).text.strip()) if soup.find('span', {'class': 'rating'}) else 0,
                'numero_resenas': int(soup.find('span', {'class': 'reviews-count'}).text.strip().split()[0]) if soup.find('span', {'class': 'reviews-count'}) else 0,
                'stock_visible': int(soup.find('span', {'class': 'stock-count'}).text.strip().split()[0]) if soup.find('span', {'class': 'stock-count'}) else 0,
                'url': url
            }
            logger.info(f"Extraído: {producto['nombre']}")
            return producto
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def insertar_en_bd(self, producto, product_id):
        try:
            cursor = self.conexion.cursor()
            query = "INSERT INTO Datos_Competencia (product_id, nombre_competidor, precio_competencia, stock_visible, valoracion, numero_resenas, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            datos = (product_id, producto.get('vendedor', 'Desconocido'), producto['precio'], producto['stock_visible'], producto['valoracion'], producto['numero_resenas'], producto['url'])
            cursor.execute(query, datos)
            self.conexion.commit()
            cursor.close()
            logger.info(f"Insertado en BD")
            return True
        except Exception as e:
            logger.error(f"Error inserción: {e}")
            return False
    
    def ejecutar_scraping(self, urls):
        for url in urls:
            logger.info(f"Scrapeando: {url}")
            producto = self.extraer_producto(url)
            if producto:
                self.insertar_en_bd(producto, 1)
            time.sleep(3)

if __name__ == "__main__":
    scraper = AliExpressScraper('localhost', 'root', '250504', 'aliexpress_vendedor')
    urls = ['https://es.aliexpress.com/item/1005007813235975.html?spm=a2g0o.tm1000026745.d0.1.54796a9aly9Wvs&pvid=944c450d-c6d4-4413-9876-4948b9c82dee&pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22sku_id%22:%2212000047460612344%22%7D&scm=1007.25281.414973.0&scm-url=1007.25281.414973.0&scm_id=1007.25281.414973.0&pdp_npi=4%40dis%21COP%21COP%2060%2C791.27%21COP%204%2C043.38%21%21%21106.76%217.10%21%402101e9a217525253670574512e52c0%2112000047460612344%21gdf%21CO%216228744897%21X&aecmd=true#nav-review']
    scraper.ejecutar_scraping(urls)