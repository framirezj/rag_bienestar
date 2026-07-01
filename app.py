import streamlit as st
import os
from dotenv import load_dotenv

# Cargar variables de entorno (como GOOGLE_API_KEY)
load_dotenv()

st.set_page_config(page_title="RAG Bienestar", page_icon="🤖", layout="centered")

st.title("🤖 Asistente Virtual de Bienestar")
st.write("Pregúntame sobre los documentos del programa de bienestar.")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del asistente (marcador de posición)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        # Aquí llamarás a tu cadena RAG:
        # response = query_rag(prompt)
        response = f"Has preguntado: '{prompt}'. (La integración RAG se conectará aquí)."
        response_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
