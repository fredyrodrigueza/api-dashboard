import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (Ancho completo)
st.set_page_config(page_title="Dashboard Errores API", layout="wide")

st.title("🚀 Análisis de Performance API: Shopify & Mercado Libre")
st.markdown("Este dashboard interactivo analiza los patrones de error para priorizar mejoras en el roadmap técnico.")

# 2. Cargar los datos resumidos
df_final = pd.read_csv('df_final.csv')
top_sh = pd.read_csv('top_sh.csv')
top_ml = pd.read_csv('top_ml.csv')

st.divider()

# ==========================================
# SECCIÓN 1: TASA DE ERROR (Gráfico a la izq, texto a la der)
# ==========================================
st.header("1. Evolución de la Tasa de Error (%)")
col1, col2 = st.columns([2, 1]) # El gráfico ocupará 2/3 y el texto 1/3

with col1:
    fig1 = px.line(df_final, x='Mes', y='Error_Rate_%', color='Event', markers=True,
                   color_discrete_sequence=['#96bf0d', '#5c6bc0'], template='plotly_white')
    fig1.update_layout(yaxis_ticksuffix="%")
    st.plotly_chart(fig1, use_container_width=True) # Muestra el gráfico interactivo

with col2:
    st.markdown("### 💡 Insights Accionables")
    st.info("**Estabilidad vs Escala:** Shopify mantiene una tasa predecible en el tiempo, pero Mercado Libre experimentó un crecimiento explosivo de sincronizaciones desde Dic 2025.")
    st.warning("**Monitoreo Sugerido:** Establecer una alerta en Datadog/CloudWatch si la tasa de error global supera el umbral del 5% en una ventana de 1 hora.")

st.divider()

# ==========================================
# SECCIÓN 2: PARETO SHOPIFY
# ==========================================
st.header("2. Principales Bloqueantes - Shopify")
col3, col4 = st.columns([2, 1])

with col3:
    fig2 = px.bar(top_sh, y='Error', x='Cantidad', orientation='h', 
                  color='Cantidad', template='plotly_white')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    st.markdown("### 💡 Insights Accionables")
    st.error("**Prioridad UX (Autenticación):** Casi 240k errores por token vencido (401 / Unauthorized). \n\n*Acción:* Enviar notificación proactiva al usuario para reconectar su cuenta antes de reintentar fallidamente.")
    st.success("**Ruido en Logs:** Más de 650k errores son por IDs genéricos (ej. 2222222222). \n\n*Acción:* Manejar silenciosamente en código (Cliente Genérico Mostrador) para limpiar las métricas.")

st.divider()

# ==========================================
# SECCIÓN 3: PARETO MERCADO LIBRE
# ==========================================
st.header("3. Principales Bloqueantes - Mercado Libre")
col5, col6 = st.columns([2, 1])

with col5:
    fig3 = px.bar(top_ml, y='Error', x='Cantidad', orientation='h', 
                  color='Cantidad', color_continuous_scale='Blues', template='plotly_white')
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

with col6:
    st.markdown("### 💡 Insights Accionables")
    st.error("**Prioridad Técnica (Rate Limiting):** Más de 46k errores `429 Too Many Requests`.\n\n*Acción:* Implementar un sistema de colas (Queues) o un patrón de reintentos *Exponential Backoff* para no saturar la API de ML.")
    st.warning("**Upselling Oportunidad:** Usuarios en 'Plan Consulta' intentando sincronizar.\n\n*Acción:* Bloquear la acción en UI y mostrar banner de Upgrade.")
