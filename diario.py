import os
import pandas as pd
from datetime import datetime

# Asegura que la carpeta 'data' exista para guardar el archivo
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def ejecutar_robot():
    # Tu lógica de scraping aquí...
    data = [{"fecha": datetime.now().strftime("%Y-%m-%d"), "detalle": "Datos del BORA"}]
    df = pd.DataFrame(data)

    # Define el nombre correcto en formato Excel (.xlsx)
    file_name = f"reporte_fenomenos_{datetime.now().strftime('%Y%m%d')}.xlsx"
    path_completo = os.path.join(DATA_DIR, file_name)

    # Guarda como Excel (requiere openpyxl)
    df.to_excel(path_completo, index=False)
    print(f"Archivo generado exitosamente en: {path_completo}")

if __name__ == "__main__":
    ejecutar_robot()