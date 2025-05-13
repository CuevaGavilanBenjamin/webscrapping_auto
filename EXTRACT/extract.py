from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
from datetime import datetime

# Configurar Chrome con user-agent
options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/123.0.0.0 Safari/537.36")

# Iniciar el navegador
driver = webdriver.Chrome(options=options)

try:
    # Entrar a la página de la SBS
    driver.get('https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx')

    # Esperar hasta que la tabla esté presente
    wait = WebDriverWait(driver, 15)
    tabla = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphContent_rgTipoCambio_ctl00"]/tbody')))

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

            if compra == "0" and venta != "0":
                compra = venta
            elif venta == "0" and compra != "0":
                venta = compra

            datos.append({
                "moneda": moneda,
                "compra": compra,
                "venta": venta
            })

    # Imprimir datos en consola
    for d in datos:
        print(d)

    # Guardar en archivo JSON
    fecha_hoy = datetime.now().strftime('%d-%m-%Y')
    ruta_carpeta = f"{fecha_hoy}/"
    os.makedirs(ruta_carpeta, exist_ok=True)
    ruta_archivo = os.path.join(ruta_carpeta, 'sbs_tipo_cambio.json')

    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f"✅ Datos guardados exitosamente en {ruta_archivo}")

except Exception as e:
    print(f"❌ Error durante la ejecución: {e}")

finally:
    driver.quit()
