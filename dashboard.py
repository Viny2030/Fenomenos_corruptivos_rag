import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ===============================
# IMPORTACIÓN DEL MOTOR RAG
# ===============================
try:
    from rag_engine import inicializar_asistente_monteverde
except Exception as e:
    st.error(f"❌ Error crítico al cargar el motor de IA: {e}")
    st.info("Revisa los imports en rag_engine.py y reconstruye el contenedor.")
    st.stop()

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(page_title="Fenómenos Corruptivos – Dashboard & IA", layout="wide")

DATA_DIR = "/app/data" if os.path.exists("/app/data") else "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

ARCHIVOS = [f for f in os.listdir(DATA_DIR) if f.endswith(".xlsx") or f.endswith(".csv")]

st.title("📉 Monitor de Fenómenos Corruptivos + IA")
st.subheader("Implementación computacional de *The Great Corruption*")

st.markdown(f"""
Este sistema analiza decisiones estatales legales según la teoría del 
**Ph.D. Vicente Humberto Monteverde**.
""")

# ===============================
# CARGA DE DATOS
# ===============================
if not ARCHIVOS:
    st.error(f"No se encontraron reportes en: {DATA_DIR}")
    st.stop()

archivo_selec = st.selectbox("Seleccioná el reporte:", sorted(ARCHIVOS, reverse=True))
ruta_completa = os.path.join(DATA_DIR, archivo_selec)

df = pd.read_excel(ruta_completa) if archivo_selec.endswith(".xlsx") else pd.read_csv(ruta_completa)

# Normalización básica
df = df.rename(columns={
    "origen": "transferencia",
    "indice_total": "indice_fenomeno_corruptivo",
    "nivel_riesgo": "nivel_riesgo_teorico"
})

# ===============================
# ASISTENTE IA
# ===============================
st.header("🤖 Asistente de Investigación")
if os.path.exists("articulo_monteverde.pdf"):
    if "asistente" not in st.session_state:
        with st.spinner("Iniciando motor de IA..."):
            st.session_state.asistente = inicializar_asistente_monteverde()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Consulta la teoría..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            respuesta = st.session_state.asistente.invoke({"input": prompt})
            full_res = respuesta["answer"]
            st.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
else:
    st.error("⚠️ Falta 'articulo_monteverde.pdf' para habilitar la IA.")

st.divider()
st.dataframe(df, use_container_width=True)
st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")