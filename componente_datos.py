import pandas as pd 
def cargar_y_validar_telemetria_grid(filepath_or_buffer) -> pd.DataFrame: #Esta linea indica que la función devuelve un DataFrame de pandas
    """Carga un archivo de telemetría de grid y valida su estructura"""
    
    # 1. Intentar la lectura del archivo o buffer
    try:# Esta linea intenta ejecutar el código dentro del bloque try. Si ocurre un error, se ejecutará el bloque except.
        df = pd.read_csv(filepath_or_buffer)#Esta linea carga un archivo CSV en un DataFrame de pandas. El parámetro filepath_or_buffer puede ser una ruta de archivo o un objeto similar a un archivo.
    except Exception as error:#Esta linea captura cualquier excepción que ocurra en el bloque try y la asigna a la variable error.
        raise ValueError(#Esta linea lanza una excepción ValueError con un mensaje personalizado que incluye el error original.
        f"No se ha podido leer el archivo de telemetría: {error}"
        ) from error#Esta linea indica que la excepción ValueError fue causada por la excepción original capturada en el bloque except.
    
    # 2. Validación estricta de presencia de las 5 columnas del contrato
    columnas_requeridas = [#Esta linea define una lista de columnas requeridas que deben estar presentes en el DataFrame.
        "timestamp",
        "fuente_generacion",
        "generacion_kwh",
        "demanda_kwh",
        "costo_mwh_eur",
        ]
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]#Esta linea crea una lista de columnas faltantes comparando las columnas requeridas con las columnas presentes en el DataFrame. Si alguna columna requerida no está presente, se agrega a la lista columnas_faltantes.
    if columnas_faltantes:#Esta linea verifica si hay columnas faltantes en la lista columnas_faltantes. Si la lista no está vacía, significa que faltan columnas requeridas.
        raise ValueError(#Esta linea lanza una excepción ValueError con un mensaje personalizado que indica que el archivo no cumple con las especificaciones del contrato y muestra las columnas faltantes.
            "El archivo no cumple con las especificaciones estrictas del contrato."
            f"Columnas faltantes: {columnas_faltantes}"#Esta linea agrega información sobre las columnas faltantes al mensaje de error.
        )
    
    # 3. Conversión de la columna timestamp a tipo datetime64[ns]
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])#Esta linea convierte la columna "timestamp" del DataFrame a un objeto datetime de pandas. Esto permite realizar operaciones de fecha y hora en esa columna.
    except Exception as error:#Esta linea captura cualquier excepción que ocurra al intentar convertir la columna "timestamp" a datetime y la asigna a la variable error.
        raise ValueError(#Esta linea lanza una excepción ValueError con un mensaje personalizado que indica que no se pudo convertir la columna "timestamp" a datetime y muestra el error original.
            f"No se ha podido convertir la columna 'timestamp' a datetime: {error}"
        ) from error#Esta linea indica que la excepción ValueError fue causada por la excepción original capturada en el bloque except.
    
    # 4. Reemplazar lecturas nulas en generación por 0.0 según el contrato
    df["generacion_kwh"] = df["generacion_kwh"] = df["generacion_kwh"].fillna(0.0)
    
    # 5. Casteo de tipos de datos de Pandas requeridos    
    try:
        df["fuente_generacion"] = df["fuente_generacion"].astype(str)
        df["generacion_kwh"] = df["generacion_kwh"].astype("float64")
        df["demanda_kwh"] = df["demanda_kwh"].astype("float64")
        df["costo_mwh_eur"] = df["costo_mwh_eur"].astype("float64")
    except Exception as error:
        raise ValueError(
            f"No se ha podido convertir las columnas a los tipos de datos esperados: {error}"
        ) from error
        
    
    # 6. Reglas de validación estricta de rangos y dominios
    fuentes_permitidas = ["Solar", "Eólica", "Bateria", "Hidro"]
    
    condicion_fuente = df["fuente_generacion"].isin(fuentes_permitidas)
    condicion_generacion = df["generacion_kwh"] >= 0.0
    condicion_demanda = df["demanda_kwh"] >= 0.0
    condicion_costo = df["costo_mwh_eur"] >= 0.0
    
    # Filtrado de registros válidos
    df_sanitizado = df[
        condicion_fuente 
        & condicion_generacion
        & condicion_demanda
        & condicion_costo
    ].copy()#Esta linea crea una copia del DataFrame original filtrando solo los registros que cumplen con todas las condiciones de validación. Esto asegura que el DataFrame resultante contenga solo datos válidos según las reglas definidas.
    
    # Verificar si el DataFrame quedó vacío tras la sanitización
    if df_sanitizado.empty:
        raise ValueError(
        "El archivo no contiene ninguna fila válida que cumpla con los límites "
        "y restricciones del contrato de datos."
    )

# 7. Restablecer índices tras descartar filas no válidas
    df_sanitizado.reset_index(drop=True, inplace=True)

    return df_sanitizado