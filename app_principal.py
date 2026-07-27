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
    
col1, col2, col3 = st.columns(3)

col1.metric(label="Ocupación Global", value="78%")
    
col2.metric(label="Camas Libres", value="15%")
col3.metric(label="Estado de Alerta", value="Normal")

