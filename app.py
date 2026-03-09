import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Errores API", layout="wide")

st.title("🚀 Análisis de Performance API: Shopify & Mercado Libre")
st.markdown("Este dashboard interactivo analiza los patrones de error para priorizar mejoras en el roadmap técnico.")

# 2. Cargar TODOS los datos resumidos
df_final = pd.read_csv('df_final.csv')
top_sh = pd.read_csv('top_sh.csv')
top_ml = pd.read_csv('top_ml.csv')
df_ml_paises = pd.read_csv('ml_paises.csv')
df_sh_ops = pd.read_csv('sh_ops.csv')
df_ml_ops = pd.read_csv('ml_ops.csv')

st.divider()

# ==========================================
# SECCIÓN 1: TASA DE ERROR
# ==========================================
st.header("1. Evolución de la Tasa de Error (%)")
col1, col2 = st.columns([2, 1])

with col1:
    fig1 = px.line(df_final, x='Mes', y='Error_Rate_%', color='Event', markers=True,
                   color_discrete_sequence=['#96bf0d', '#5c6bc0'], template='plotly_white')
    fig1.update_layout(yaxis_ticksuffix="%")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 💡 Insights Accionables")
    st.info("**Estabilidad vs Escala:** Shopify mantiene una tasa predecible en el tiempo, pero Mercado Libre experimentó un crecimiento explosivo de sincronizaciones desde Dic 2025.(Los datos de errores de conexión están disponibles a partir de noviembre 25)")
    st.warning("**Monitoreo Sugerido:** Establecer una alerta en Datadog/CloudWatch si la tasa de error global supera el umbral del 5% en una ventana de 1 hora.")

st.divider()

# ==========================================
# SECCIÓN 2: PARETO DE ERRORES (Causas Principales)
# ==========================================
st.header("2. Principales Bloqueantes por Plataforma")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Shopify")
    fig2 = px.bar(top_sh, y='Error', x='Cantidad', orientation='h', 
                  color='Cantidad', template='plotly_white')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)
    st.error("**Prioridad UX (Autenticación):** Casi 240k errores por token vencido (401 / Unauthorized). *Acción:* Notificación proactiva para reconectar cuenta.")

with col4:
    st.subheader("Mercado Libre")
    fig3 = px.bar(top_ml, y='Error', x='Cantidad', orientation='h', 
                  color='Cantidad', color_continuous_scale='Blues', template='plotly_white')
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)
    st.error("**Prioridad Técnica (Rate Limiting):** Más de 46k errores `429 Too Many Requests`. *Acción:* Implementar colas o Exponential Backoff.")

st.divider()

# ==========================================
# SECCIÓN 3: PATRONES GEOGRÁFICOS (MERCADO LIBRE)
# ==========================================
st.header("3. Patrones Geográficos (Mercado Libre)")

st.warning("**El elefante en la habitación (Sin País: ~549k):** El 95% de los errores no tienen un país asociado. ¿Por qué? Porque errores masivos como el Rate Limiting (429) o Bloqueo por Plan Consulta ocurren a nivel de conexión de la cuenta, antes de que el sistema siquiera intente leer de qué país es el usuario o el producto.")

col_map1, col_map2 = st.columns([1, 1])

with col_map1:
    fig_paises = px.bar(df_ml_paises, x='País', y='Cantidad', 
                        title="Distribución de Errores por País Identificado",
                        color='Cantidad', color_continuous_scale='Teal', template='plotly_white')
    st.plotly_chart(fig_paises, use_container_width=True)

with col_map2:
    st.markdown("<br><br>", unsafe_allow_html=True) # Espacio para alinear
    st.success("**El foco operativo (Colombia):** De los errores que *sí* logran llegar al nivel del recurso (donde importa la validación local), Colombia domina abrumadoramente. \n\n*Acción:* Cualquier esfuerzo para arreglar validaciones de campos (dirección, régimen) debe priorizar las reglas de negocio de Colombia.")

st.divider()

# ==========================================
# SECCIÓN 4: PATRONES POR OPERACIÓN
# ==========================================
st.header("4. Patrones por Tipo de Operación (Impacto en Negocio)")
col_op1, col_op2 = st.columns(2)

with col_op1:
    fig_sh_ops = px.bar(df_sh_ops, x='Operación', y='Cantidad', 
                        title="Top 5 Operaciones Afectadas (Shopify)",
                        color='Cantidad', color_continuous_scale='Greens', template='plotly_white')
    st.plotly_chart(fig_sh_ops, use_container_width=True)
    st.info("**Impacto Shopify:** Casi 1M de errores en la creación/actualización de clientes (ruido por IDs genéricos), pero la verdadera hemorragia está en los **238k fallos en orders/create**, lo que significa facturación e inventario desfasado.")

with col_op2:
    fig_ml_ops = px.bar(df_ml_ops, x='Operación', y='Cantidad', 
                        title="Top 5 Operaciones Afectadas (Mercado Libre)",
                        color='Cantidad', color_continuous_scale='Blues', template='plotly_white')
    st.plotly_chart(fig_ml_ops, use_container_width=True)
    st.info("**Impacto Mercado Libre:** La gran mayoría de bloqueos ocurren al sincronizar `items` (catálogo/stock), lo cual detona el Rate Limiting. Sin embargo, hay **9,880 facturas fallidas (`invoice`)**, un riesgo altísimo de retención que genera tickets de soporte.")

