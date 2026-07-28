import pandas as pd


def calcular_kpis_hospitalarios(df: pd.DataFrame) -> dict:
    """
    Calcula los principales KPIs hospitalarios.

    Parámetro:
        df (pd.DataFrame): DataFrame previamente validado.

    Retorna:
        dict: Diccionario con los KPIs calculados.
    """
    # Suma de camas ocupadas y camas instaladas

    total_camas_ocupadas = df["camas_ocupadas"].sum()
    total_camas_instaladas = df["camas_instaladas"].sum()

    # 1. Ocupación promedio (%)

    ocupacion_promedio_pct = (
        (total_camas_ocupadas / total_camas_instaladas) * 100
        if total_camas_instaladas > 0
        else 0.0
    )

    # 2. Costo total

    costo_total = df["costo_operativo_dia"].sum()

    # 3. Camas libres
    camas_libres = int(total_camas_instaladas - total_camas_ocupadas)

    # 4. Estado de alerta
    if ocupacion_promedio_pct >= 85.0:
        estado_alerta = "CRÍTICO (Saturación)"
    else:
        estado_alerta = "Normal (Capacidad Estable)"

    # Retornar los KPIs en un diccionario

    return {
        "ocupacion_promedio_pct": float(ocupacion_promedio_pct),
        "costo_total": float(costo_total),
        "camas_libres": camas_libres,
        "estado_alerta": estado_alerta
    }

# Bloque de prueba

if __name__ == "__main__":

    datos = {
        "camas_instaladas": [100, 80, 120],
        "camas_ocupadas": [90, 60, 100],
        "costo_operativo_dia": [5000, 4000, 7000]
    }

    df = pd.DataFrame(datos)

    resultado = calcular_kpis_hospitalarios(df)

    print("KPIs Hospitalarios")
    print("------------------")
    print(resultado)


