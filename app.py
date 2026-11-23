import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Título de la aplicación
st.title("📊 Simulación de 100,000 Escenarios Financieros")
st.write("Esta app calcula y grafica 100,000 escenarios posibles de rendimiento de una inversión.")

# --- PASO 1: Generar los 100,000 escenarios ---
# Usamos @st.cache_data para que Streamlit calcule esto UNA SOLA VEZ.
# Si no lo pones, tardaría segundos cada vez que muevas un filtro.
@st.cache_data
def generar_escenarios():
    np.random.seed(42) # Para que los números sean siempre los mismos al recargar
    # Simulamos 100,000 rendimientos anuales (media 5%, variación 15%)
    rendimientos = np.random.normal(loc=0.05, scale=0.15, size=100000)
    
    df = pd.DataFrame({
        'ID_Escenario': range(1, 100001),
        'Rendimiento (%)': rendimientos * 100
    })
    return df

df_completo = generar_escenarios()

# --- PASO 2: Crear los controles dinámicos (Interactividad) ---
st.sidebar.header("🎛️ Filtros Dinámicos")
st.sidebar.write("Mueve las barras para filtrar los 100,000 escenarios:")

minimo = st.sidebar.slider("Rendimiento Mínimo (%)", -50.0, 50.0, -10.0)
maximo = st.sidebar.slider("Rendimiento Máximo (%)", -50.0, 50.0, 20.0)

# --- PASO 3: Filtrar los datos en tiempo real ---
df_filtrado = df_completo[
    (df_completo['Rendimiento (%)'] >= minimo) & 
    (df_completo['Rendimiento (%)'] <= maximo)
]

# Mostrar cuántos escenarios estamos viendo
st.metric(label="Escenarios visibles", value=f"{len(df_filtrado):,} de 100,000")

# --- PASO 4: Gráfico dinámico con Plotly ---
st.subheader("Distribución de los Escenarios Filtrados")

# Creamos el histograma. Plotly es súper rápido para esto.
fig = px.histogram(
    df_filtrado, 
    x='Rendimiento (%)', 
    nbins=100, 
    color_discrete_sequence=['#636EFA'],
    title="Histograma de Rendimientos"
)

# Actualizamos el diseño para que se vea profesional
fig.update_layout(
    xaxis_title="Rendimiento (%)",
    yaxis_title="Cantidad de Escenarios",
    bargap=0.1
)

# Lo mostramos en Streamlit (use_container_width=True lo hace responsivo)
st.plotly_chart(fig, use_container_width=True)

# --- PASO 5: Mostrar la tabla de datos (Opcional) ---
with st.expander("🔍 Ver tabla de datos filtrada"):
    st.dataframe(df_filtrado, use_container_width=True)