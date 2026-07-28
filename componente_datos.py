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
    # 3. Regla Estricta: No nulos en la fecha
    if df["fecha_ingreso"].isna().any():
        raise ValueError("Contrato incumplido: La columna 'fecha_ingreso' contiene valores nulos")
    
    try:
        df["fecha_ingreso"] = pd.to_datetime(df["fecha_ingreso"])
        df["area_hospital"] = df["area_hospital"].astype(str)
        df["camas_ocupadas"] = df["camas_ocupadas"].astype("int64")
        df["camas_totales"] = df["camas_totales"].astype("int64")
        df["costo_operativo_dia"] = df["costo_operativo_dia"].astype("float64")
    except Exception as error:
        raise ValueError(f"Contrato incumplido: Error al convertir los tipos de datos")
    
    # 5. Validacion de Reglas Logicas y Matematicas
    
    # - No se permiten fechas futuras
    fecha_actual = pd.Timestamp.today().normalize()
    if (df["fecha_ingreso"] > fecha_actual).any():
        raise ValueError("Contrato incumplido: Existen registros con fechas futuras.")
    
    # - Valores exactos para area hospital
    areas_validas = ["Urgencias", "UCI", "Planta"]
    if not df["area_hospital"].isin(areas_validas).all():
        raise ValueError(f"Contrato incumplido: 'area_hospital' tiene valores invalidos")
    
    # - camas_totales debe ser mayor a 0
    if (df["camas_totales"] <= 0).any():
        raise ValueError("Contrato incumplido: Existen registros con 'camas_totales' igual o menor a 0.")

    # - camas_ocupadas entre 0 y camas_totales
    condicion_ocupadas = (df["camas_ocupadas"] >= 0) & (df["camas_ocupadas"] <= df["camas_totales"])
    if not condicion_ocupadas.all():
        raise ValueError("Contrato incumplido: 'camas_ocupadas' es menor a 0 o supera la capacidad máxima de 'camas_totales'.")

    # - costo_operativo_dia mayor o igual a 0.0
    if (df["costo_operativo_dia"] < 0.0).any():
        raise ValueError("Contrato incumplido: Existen registros con un 'costo_operativo_dia' negativo.")

    # 6. Salida: Retornar el DataFrame validado si pasa todas las pruebas
    return df