from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.chrome.options import Options
import os
import json
from datetime import datetime
import time

# Configurar Chrome en modo headless para entornos como GitHub Actions
options = Options()
options.add_argument('--headless=new')  # Nuevo headless compatible
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Iniciar el navegador con opciones configuradas
driver = webdriver.Chrome(options=options)

# Entrar a la página de la SBS
driver.get('https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx')
time.sleep(3)  # Esperar a que cargue

# Obtener la tabla de tipos de cambio
tbody = driver.find_element(By.XPATH, '//*[@id="ctl00_cphContent_rgTipoCambio_ctl00"]/tbody')

# Encontrar todas las filas
filas = tbody.find_elements(By.TAG_NAME, 'tr')

# Extraer datos
datos = []
for fila in filas:
    columnas = fila.find_elements(By.TAG_NAME, 'td')
    if len(columnas) == 3:
        moneda = columnas[0].text.strip()
        compra = columnas[1].text.strip()
        venta = columnas[2].text.strip()
        if compra == "0" and venta != "0":
            compra = venta
        elif venta == "0" and compra != "0":
            venta = compra
        datos.append({
            "moneda": moneda,
            "compra": compra,
            "venta": venta
        })

# Mostrar datos en consola
for d in datos:
    print(d)

# Cerrar navegador
driver.quit()

# Guardar archivo JSON con la fecha actual como nombre de carpeta
fecha_hoy = datetime.now().strftime('%d-%m-%Y')
ruta_carpeta = f"{fecha_hoy}/"
os.makedirs(ruta_carpeta, exist_ok=True)
ruta_archivo = os.path.join(ruta_carpeta, 'sbs_tipo_cambio.json')

with open(ruta_archivo, 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=4, ensure_ascii=False)

print(f"Datos guardados exitosamente en {ruta_archivo}")
