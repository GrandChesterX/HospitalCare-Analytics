import pandas as pd

def calcular_kpis_hospitalarios(df: pd.DataFrame) -> dict:
    """
    Calcula los principales KPIs hospitalarios.
    """
    # 1. Sumar las camas ocupadas

    total_camas_ocupadas = df["camas_ocupadas"].sum()

    # 2. Sumar las camas totales

    total_camas_totales = df["camas_totales"].sum()

    # 3. Calcular el porcentaje de ocupación

    if total_camas_totales > 0:
        ocupacion_promedio_pct = (
            total_camas_ocupadas / total_camas_totales
        ) * 100
    else:
        ocupacion_promedio_pct = 0.0

    # 4. Calcular el costo total

    costo_total = df["costo_operativo_dia"].sum()

    # 5. Calcular las camas libres

    camas_libres = int(total_camas_totales - total_camas_ocupadas)

    # 6. Determinar el estado de alerta

    if ocupacion_promedio_pct >= 85.0:
        estado_alerta = "CRÍTICO (Saturación)"
    else:
        estado_alerta = "Normal (Capacidad Estable)"

    # 7. Devolver los resultados
    return {
        "ocupacion_promedio_pct": float(ocupacion_promedio_pct),
        "costo_total": float(costo_total),
        "camas_libres": camas_libres,
        "estado_alerta": estado_alerta
    }

# Bloque de prueba
if __name__ == "__main__":

    datos = {
        "camas_totales": [100, 80, 120],
        "camas_ocupadas": [90, 60, 100],
        "costo_operativo_dia": [5000, 4000, 7000]
    }

    df = pd.DataFrame(datos)

    resultado = calcular_kpis_hospitalarios(df)

    print("KPIs Hospitalarios")
    print("------------------")
    print(f"Ocupación promedio: {resultado['ocupacion_promedio_pct']:.2f}%")
    print(f"Costo total: ${resultado['costo_total']:.2f}")
    print(f"Camas libres: {resultado['camas_libres']}")
    print(f"Estado de alerta: {resultado['estado_alerta']}")