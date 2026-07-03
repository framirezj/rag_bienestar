import streamlit as st
import os
from dotenv import load_dotenv

from src.rag import get_rag_chain

# Cargar variables de entorno (como GOOGLE_API_KEY)
load_dotenv()

st.set_page_config(page_title="RAG Bienestar", page_icon="🤖", layout="centered")

st.title("🤖 Asistente Virtual de Bienestar")
st.write("Pregúntame sobre los documentos del programa de bienestar.")

# Cargar la cadena RAG y guardarla en caché
@st.cache_resource
def load_rag():
    return get_rag_chain()

try:
    rag_chain = load_rag()
except Exception as e:
    st.error(f"Error al cargar la base de datos vectorial. ¿Ejecutaste el indexador primero? Detalle: {e}")
    st.stop()

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

    # Respuesta del asistente
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        with st.spinner("Pensando..."):
            try:
                response_data = rag_chain.invoke({"input": prompt})
                response = response_data["answer"]
            except Exception as e:
                response = f"Ocurrió un error al procesar la respuesta: {e}"
                
        response_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

