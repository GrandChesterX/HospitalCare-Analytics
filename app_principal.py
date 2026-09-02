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
        # Creamos un contenedor vacío para atrapar la basura visual
        contenedor_trampa = st.empty()
        
        # Ejecutamos la función dentro del contenedor
        with contenedor_trampa:
            st.session_state['data_limpia'] = cd.cargar_y_validar_datos_hospital(archivo_subido)
            
        # Vaciamos el contenedor, borrando el texto que inyectó el componente
        contenedor_trampa.empty() 
        
    except ValueError as e:
        st.error(f"❌ Error en los datos: {e}")
else:
    st.info("Porfavor sube el archivo CSV")

    st.info("Por favor sube el archivo CSV")



if 'data_limpia' not in st.session_state:
    st.warning("Tienes que subir el archivo CSV")
    #st.stop()

    
try:
    # Le pasamos el DataFrame limpio que guardamos en session_state
    kpis = cm.calcular_kpis_hospitalarios(st.session_state['data_limpia'])
    
    col1, col2, col3, col4 = st.columns(4)
    # Usamos las claves exactas que le exigimos a Carlos en el README
    col1.metric(label="Ocupación Global", value=f"{kpis['ocupacion_promedio_pct']}%")
    col2.metric(label="Camas Libres", value=kpis['camas_libres'])
    col3.metric(label="Estado de Alerta", value=kpis['estado_alerta'])
    col4.metric(label="Gasto Total (€)", value=f"{kpis['costo_total']:,.2f}")


except AttributeError:
    # Si Carlos aún no ha subido su función, mostramos esto:
    st.info("⏳ Esperando el módulo de métricas (Carlos)...")
except Exception as e:
    # Si la función de Carlos tiene un error interno:
    st.error(f"❌ Error en el cálculo de KPIs: {e}")

st.markdown("---")
st.subheader("📈 Proyección de Demanda (Próximos 7 días)")


try:
    # 1. Instanciamos la clase del motor predictivo
    motor = cp.MotorPredictivo()
    
    # 2. Le pasamos el DataFrame limpio al método de la clase
    predicciones = motor.predecir_demanda_camas(st.session_state['data_limpia'])
    
    # Convertimos la lista en un DataFrame pequeño para graficar
    df_prediccion = pd.DataFrame(predicciones, columns=["Camas Requeridas"])
    df_prediccion.index = range(1, len(predicciones) + 1) # Nombramos los días del 1 al 7
    
    # Dibujamos el gráfico de líneas
    st.line_chart(df_prediccion)

except AttributeError:
    st.info("⏳ Esperando el motor predictivo de demanda...")
except Exception as e:
    st.error(f"❌ Error al calcular la predicción: {e}")