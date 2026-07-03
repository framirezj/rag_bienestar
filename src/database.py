import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configuración de rutas
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
VS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vectorstore")

def build_vector_store():
    """
    Carga los documentos de 'data/', los fragmenta, genera embeddings
    y guarda la base de datos vectorial FAISS en 'vectorstore/'.
    """
    # 1. Cargar documentos
    loader = PyPDFDirectoryLoader(DATA_DIR)
    docs = loader.load()
    
    # 2. Fragmentar textos
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = text_splitter.split_documents(docs)
    
    # 3. Embeddings y Vector Store
    model_embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.from_documents(chunks, model_embeddings)
    vector_store.save_local(VS_DIR)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Iniciando la carga de documentos y generación de embeddings...")
    try:
        build_vector_store()
        print("¡Base de datos vectorial creada con éxito y guardada en 'vectorstore/'!")
    except Exception as e:
        print(f"Error al construir la base de datos vectorial: {e}")

#uv run python src/database.py