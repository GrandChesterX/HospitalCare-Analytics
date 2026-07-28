import numpy as np
import pandas as pd


class MotorPredictivo:
    """Clase encargada de la proyección de demanda hospitalaria utilizando

    modelos estadísticos y aleatorización controlada.
    """

    def __init__(
        self, ventana_tendencia: int = 5, factor_ruido: float = 0.05
    ):
        """Inicializa el motor predictivo.

        :param ventana_tendencia: Número de últimos registros para calcular la
        tendencia.
        :param factor_ruido: Porcentaje de variabilidad probabilística (ej.
        0.05 = 5%).
        """
        self.ventana_tendencia = ventana_tendencia
        self.factor_ruido = factor_ruido

    def _calcular_promedio_movil_ponderado(self, series: pd.Series) -> float:
        """Calcula el promedio móvil ponderado dando más peso a los datos más

        recientes.
        """
        valores = series.tail(self.ventana_tendencia).values
        n = len(valores)

        if n == 0:
            return 0.0

        # Crear pesos lineales (ej. para 5 días: 1, 2, 3, 4, 5)
        pesos = np.arange(1, n + 1)
        promedio_ponderado = np.sum(valores * pesos) / np.sum(pesos)

        return float(promedio_ponderado)

    def predecir_demanda_camas(
        self, df: pd.DataFrame, dias_proyeccion: int = 7
    ) -> list[int]:
        """Proyecta la cantidad de camas requeridas para los próximos N días.

        :param df: DataFrame que debe contener una columna con el histórico de
        camas ocupadas.
        :param dias_proyeccion: Número de días a predecir.
        :return: Lista de enteros con las camas proyectadas por día.
        """
        # Nota: Asumimos que el DataFrame tiene una columna numérica representativa.
        # Ajusta el nombre de la columna ('camas_ocupadas') según tu estructura de datos.
        columna_camas = (
            "camas_ocupadas" if "camas_ocupadas" in df.columns else df.columns[-1]
        )

        # 1. Obtener la base de la tendencia actual
        linea_base = self._calcular_promedio_movil_ponderado(df[columna_camas])

        proyecciones = []

        # 2. Generar la predicción agregando ruido probabilístico
        for _ in range(dias_proyeccion):
            # Definir los límites del ruido basado en el factor de variabilidad
            delta_maximo = linea_base * self.factor_ruido
            ruido = np.random.uniform(-delta_maximo, delta_maximo)

            # Aplicar la predicción y asegurar que no existan camas negativas
            prediccion_dia = max(0, round(linea_base + ruido))
            proyecciones.append(prediccion_dia)

            # Opcional: Actualizar la línea base autoregresivamente para los siguientes días
            # Descomenta la siguiente línea si quieres que la predicción evolucione día a día:
            # linea_base = prediccion_dia

        return proyecciones


    # Simulación de datos históricos (últimos 10 días de camas ocupadas)
datos_ejemplo = pd.DataFrame({"camas_ocupadas": [45, 48, 50, 47, 52, 55, 53, 58, 60, 62]})

# Instanciar el componente de POO
motor = MotorPredictivo(ventana_tendencia=5, factor_ruido=0.08)

# Ejecutar la función requerida
resultado = motor.predecir_demanda_camas(datos_ejemplo, dias_proyeccion=7)

print("Proyección de camas para los próximos 7 días:")
print(resultado)
# Salida esperada: Lista de 7 enteros, ej. [60, 57, 61, 59, 63, 58, 60]