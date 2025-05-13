import pandas as pd
import os
from datetime import datetime
from zoneinfo import ZoneInfo  # disponible desde Python 3.9
# Directorio de los datos
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'EXTRACT')
print("ESTA ES LA RUTA +++", base_path)


# Obtener la fecha actual para el reporte
hoy = datetime.now(ZoneInfo("America/Lima")).strftime('%d-%m-%Y')

# Lista para almacenar los DataFrames
all_data = []

# Recorre todas las carpetas (fechas) de la estructura
for folder_name in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder_name)
    
    # Verificar que sea una carpeta con datos
    if os.path.isdir(folder_path):
        try:
            # Intentar cargar el archivo JSON
            df = pd.read_json(os.path.join(folder_path, 'sbs_tipo_cambio.json'))
            df["Fecha"]=folder_name
            all_data.append(df)
        except:
            print(f"No se pudo leer el archivo para {folder_name}")
print(all_data)
# Concatenar todos los DataFrames en uno solo
final_df = pd.concat(all_data, ignore_index=True)
script_dir = os.path.dirname(os.path.abspath(__file__))
ruta_archivo=os.path.join(script_dir,"reporte_consolidado.csv")
# Guardar el archivo CSV consolidado
final_df.to_csv(ruta_archivo, index=False)

print (base_path)