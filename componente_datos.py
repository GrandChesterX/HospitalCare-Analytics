import pandas as pd
from datetime import datetime

def cargar_y_datos_hospital(filepath_or_buffer) -> pd.DataFrame:
    """
    Carga y valida los registros de las camas ocupadas en el hospital desde un CSV
    o buffer.
    Verifica que la información cumpla estrictamente con el Contrato de Datos
    
    """
    # 1. Ingesta: Intentar leer el archivo CSV
    try:
        df = pd.read_csv(filepath_or_buffer)
    except Exception as error:
        raise ValueError(f"Error crítico al leer el archivo CSV: {error}")
    
    # 2. Validación de presencia de columnas exactas
    columnas_separadas = [
        "fecha_ingreso",
        "area_hospital",
        "camas_ocupadas",
        "camas_totales",
        "costo_operativo_dia"
    ]
    
    
    faltantes = [col for col in columnas_separadas if col not in df.columns]
    if faltantes:
        raise ValueError(
            f"Contrato incumplido. Faltan las siguientes columnas "
        )