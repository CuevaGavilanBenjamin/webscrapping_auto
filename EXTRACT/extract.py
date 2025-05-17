from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from zoneinfo import ZoneInfo

# Configurar Chrome con user-agent
options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/123.0.0.0 Safari/537.36")

# Iniciar el servicio de ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Entrar a la página de la SBS
    driver.get('https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx')

    # Esperar hasta que la tabla esté presente
    wait = WebDriverWait(driver, 15)
    tabla = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphContent_rgTipoCambio_ctl00"]/tbody')))

    # Verificar si hay mensaje de "No existe información para la fecha elegida"
    mensaje_no_data = tabla.find_elements(By.XPATH, './/tr[@class="rgNoRecords"]/td/div')
    if mensaje_no_data and "No existe información para la fecha elegida" in mensaje_no_data[0].text:
        print("No hay información para la fecha elegida. No se extraerán datos.")
    else:
        # Extraer las filas
        filas = tabla.find_elements(By.TAG_NAME, 'tr')

        # Procesar datos
        datos = []
        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, 'td')
            if len(columnas) == 3:
                moneda = columnas[0].text.strip()
                compra = columnas[1].text.strip()
                venta = columnas[2].text.strip()
                # Si alguna celda está vacía, se copia el valor de la otra
                if compra == "" and venta != "":
                    compra = venta
                elif venta == "" and compra != "":
                    venta = compra

                datos.append({
                    "moneda": moneda,
                    "compra": compra,
                    "venta": venta
                })

        # Imprimir datos en consola
        for d in datos:
            print(d)

        # Obtener la fecha actual en zona horaria de Lima
        fecha = datetime.now(ZoneInfo("America/Lima"))
        anio = fecha.strftime('%Y')           # Ej: '2025'
        mes = fecha.strftime('%m')            # Ej: '05'
        dia = fecha.strftime('%d-%m-%Y')      # Ej: '17-05-2025'

        # Construir ruta completa: EXTRACT/año/mes/día
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta = os.path.join(script_dir, '..', 'EXTRACT', anio, mes, dia)
        os.makedirs(ruta_carpeta, exist_ok=True)

        # Ruta completa del archivo
        ruta_archivo = os.path.join(ruta_carpeta, 'sbs_tipo_cambio.json')
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        print(f"Datos guardados exitosamente en {ruta_archivo}")

except Exception as e:
    print(f"Error durante la ejecución: {e}")

finally:
    driver.quit()
