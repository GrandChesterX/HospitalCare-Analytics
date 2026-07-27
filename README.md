# HospitalCare Analytics
Proyecto HospitalCare Analytics
# HospitalCare Analytics - Guía de Desarrollo por Componentes (DSBC)

Este documento detalla las responsabilidades técnicas de cada miembro del Equipo 1. Para garantizar que el proyecto se integre correctamente en `app_principal.py`, es **obligatorio** respetar los nombres de las funciones, los tipos de datos de entrada/salida y las reglas de negocio descritas a continuación.

**Nota importante de arquitectura:** Está estrictamente prohibido el uso de variables globales fuera de las funciones modulares. Todo el código debe estar encapsulado.

---

## 1. Módulo de Datos (Ingesta y Validación)
**Responsable:** Juanjo (Data Engineer)  
**Rama:** `feature/ingesta-datos`  
**Archivo:** `componente_datos.py`

Debes programar la lógica para cargar el CSV y asegurar que la información cumpla con el Contrato de Datos antes de pasar a los demás módulos.

* **Función a crear:** `cargar_y_validar_datos_hospital(filepath_or_buffer)`
* **Entrada:** Ruta del archivo o buffer en memoria (proveniente de Streamlit).
* **Salida:** `pandas.DataFrame` limpio y validado.
* **Reglas Estrictas del Contrato:**
  1. `fecha_ingreso`: Tipo datetime. No debe contener valores nulos ni fechas futuras.
  2. `area_hospital`: Tipo string. Solo admite los valores exactos: **"Urgencias"**, **"UCI"** o **"Planta"**.
  3. `camas_ocupadas`: Tipo entero. Debe ser mayor o igual a 0, y menor o igual a `camas_totales`.
  4. `camas_totales`: Tipo entero. Debe ser mayor a 0.
  5. `costo_operativo_dia`: Tipo flotante. Debe ser mayor o igual a **0.0**.
* **Manejo de Errores:** Si el archivo no tiene estas 5 columnas exactas o los datos rompen las reglas, la función debe lanzar una excepción `ValueError` con un mensaje descriptivo.

---

## 2. Módulo de Lógica (Métricas y KPIs)
**Responsable:** Carlos (Backend / Data Scientist)  
**Rama:** `feature/logica-prediccion`  
**Archivo:** `componente_metricas.py`

Debes procesar el DataFrame validado para extraer los indicadores clave del hospital.

* **Función a crear:** `calcular_kpis_hospitalarios(df: pd.DataFrame)`
* **Entrada:** DataFrame (ya validado por el componente 1).
* **Salida:** Un diccionario de Python (`dict`) que contenga **exactamente** estas 4 claves:
  * `ocupacion_promedio_pct`: (Float) Calculado con la fórmula matemática:
    $Ocupacion = \frac{\sum camas\_ocupadas}{\sum camas\_totales} \times 100$
  * `costo_total`: (Float) La suma de toda la columna `costo_operativo_dia`.
  * `camas_libres`: (Int) La diferencia total entre las camas instaladas y las ocupadas.
  * `estado_alerta`: (String) Si la `ocupacion_promedio_pct` es mayor o igual a **85.0%**, el valor debe ser **"CRÍTICO (Saturación)"**. En caso contrario, debe ser **"Normal (Capacidad Estable)"**.

---

## 3. Módulo Predictivo (Proyección de Demanda)
**Responsable:** Milán (Backend / Data Scientist)  
**Rama:** `feature/logica-prediccion`  
**Archivo:** `componente_prediccion.py`

Debes construir el motor que estime cuántas camas se necesitarán en los próximos días basándose en el histórico.

* **Función a crear:** `predecir_demanda_camas(df: pd.DataFrame, dias_proyeccion: int = 7)`
* **Entrada:** DataFrame validado y un entero con los días a proyectar (por defecto 7).
* **Salida:** Una lista de enteros (`list[int]`) donde cada número representa la cantidad de camas requeridas para cada uno de los días proyectados.
* **Algoritmo requerido:** Debes implementar una extrapolación basada en el promedio móvil ponderado de la tendencia de los últimos 5 registros, añadiendo un factor de ruido de variabilidad probabilística para simular fluctuaciones reales.