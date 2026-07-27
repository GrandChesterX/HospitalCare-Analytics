import streamlit as st
import pandas as pd
#Importamos los módulos del equipo
import componente_datos as cd
import componente_metricas as cm
import componente_prediccion as cp

st.set_page_config(page_title="HospitalCare Analytics", page_icon="🏥", layout="wide")
st.title("🏥 Dashboard de Ocupación - HospitalCare Analytics")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuración")
    archivo_subido = st.file_uploader("Sube el archivo CSV del hospital", type=["csv"])
    
if archivo_subido is not None:
    try:
        st.session_state['data_limpia'] = cd.cargar_y_validar_datos_hospital(archivo_subido)
    except ValueError as e:
        st.error(f"❌ Error en los datos: {e}")
else:
    st.info("Porfavor sube el archivo CVS")


if 'data_limpia' not in st.session_state:
    st.warning("Tienes que subir el archivo CVS")
    #st.stop()

    
try:
    # Le pasamos el DataFrame limpio que guardamos en session_state
    kpis = cm.calcular_kpis_hospitalarios(st.session_state['data_limpia'])
    
    col1, col2, col3 = st.columns(3)
    # Usamos las claves exactas que le exigimos a Carlos en el README
    col1.metric(label="Ocupación Global", value=f"{kpis['ocupacion_promedio_pct']}%")
    col2.metric(label="Camas Libres", value=kpis['camas_libres'])
    col3.metric(label="Estado de Alerta", value=kpis['estado_alerta'])

except AttributeError:
    # Si Carlos aún no ha subido su función, mostramos esto:
    st.info("⏳ Esperando el módulo de métricas (Carlos)...")
except Exception as e:
    # Si la función de Carlos tiene un error interno:
    st.error(f"❌ Error en el cálculo de KPIs: {e}")

st.markdown("---")
st.subheader("📈 Proyección de Demanda (Próximos 7 días)")


try:
    # Le pasamos el DataFrame limpio a la función de Milán
    predicciones = cp.predecir_demanda_camas(st.session_state['data_limpia'])
    
    # Convertimos la lista de Milán en un DataFrame pequeño para graficar
    df_prediccion = pd.DataFrame(predicciones, columns=["Camas Requeridas"])
    df_prediccion.index = range(1, len(predicciones) + 1) # Nombramos los días del 1 al 7
    
    # Dibujamos el gráfico de líneas
    st.line_chart(df_prediccion)

except AttributeError:
    # Si Milán aún no ha subido su función
    st.info("⏳ Esperando el motor predictivo de demanda (Milán)...")
except Exception as e:
    # Si hay algún error dentro de la función de Milán
    st.error(f"❌ Error al calcular la predicción: {e}")