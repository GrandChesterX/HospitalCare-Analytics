import pandas as pd
import numpy as np
from typing import List  # Soluciona el error en Python < 3.9

class MotorPredictivoInterno:
    """Clase existente que contiene la lógica interna de predicción."""
    
    def __init__(self):
        pass

    def calcular_proyeccion(self, df: pd.DataFrame, dias_proyeccion: int) -> List[int]:
        # Validar que la columna requerida exista en el DataFrame
        if 'camas_ocupadas' not in df.columns:
            raise KeyError("El DataFrame debe contener la columna 'camas_ocupadas'.")

        # Validar que existan suficientes datos para el promedio móvil
        if len(df) < 5:
            raise ValueError("El DataFrame debe contener al menos 5 registros para calcular la tendencia.")
            
        # Tomar los últimos 5 registros de la columna de demanda
        ultimos_datos = df['camas_ocupadas'].tail(5).to_numpy()
        
        # Definir pesos para el promedio móvil ponderado
        pesos = np.array([1, 2, 3, 4, 5])
        promedio_ponderado = np.average(ultimos_datos, weights=pesos)
        
        # Calcular la variabilidad
        desviacion = np.std(ultimos_datos) if np.std(ultimos_datos) > 0 else 1.0
        
        proyeccion = []
        ultima_prediccion = promedio_ponderado
        
        # Generar la extrapolación día a día
        for _ in range(dias_proyeccion):
            ruido = np.random.normal(0, desviacion * 0.1) 
            prediccion_dia = max(0, int(round(ultima_prediccion + ruido)))
            proyeccion.append(prediccion_dia)
            ultima_prediccion = prediccion_dia 
            
        return proyeccion

# =====================================================================
# INTERFAZ PÚBLICA REQUERIDA POR EL CONTRATO
# =====================================================================

def predecir_demanda_camas(df: pd.DataFrame, dias_proyeccion: int = 7) -> List[int]:
    """
    Función principal expuesta a nivel de módulo.
    """
    motor = MotorPredictivoInterno()
    return motor.calcular_proyeccion(df, dias_proyeccion)