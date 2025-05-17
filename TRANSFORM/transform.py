import pandas as pd
import os
from datetime import datetime
from zoneinfo import ZoneInfo  

# Ruta base de EXTRACT
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'EXTRACT')
print("🔍 Explorando en:", base_path)

# Obtener fecha actual en zona horaria de Lima
hoy = datetime.now(ZoneInfo("America/Lima")).strftime('%d-%m-%Y')

# Lista para guardar todos los dataframes
all_data = []

# Recorrer todas las carpetas y subcarpetas de EXTRACT
for root, dirs, files in os.walk(base_path):
    if 'sbs_tipo_cambio.json' in files:
        try:
            ruta_archivo = os.path.join(root, 'sbs_tipo_cambio.json')
            df = pd.read_json(ruta_archivo)

            # Extraer la fecha desde el nombre de la carpeta más profunda
            fecha = os.path.basename(root)
            df['Fecha'] = fecha

            all_data.append(df)
        except Exception as e:
            print(f"No se pudo leer el archivo en {root}: {e}")

# Combinar todos los dataframes
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    # Guardar en TRANSFORM/reporte_consolidado.csv
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_salida = os.path.join(script_dir, "reporte_consolidado.csv")
    final_df.to_csv(ruta_salida, index=False)

    print(f"Reporte consolidado guardado en: {ruta_salida}")
else:
    print("No se encontraron archivos para consolidar.")
