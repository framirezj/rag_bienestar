import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

VS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vectorstore")

def get_rag_chain():
    """
    Carga la base de datos vectorial FAISS y retorna la cadena RAG configurada.
    """
    # 1. Cargar embeddings y base de datos vectorial
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db = FAISS.load_local(VS_DIR, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 4})
    
    # 2. Inicializar LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
    # 3. Crear Prompt Template y Cadena RAG
    system_prompt = (
        "Eres un asistente virtual experto en el Programa de Bienestar de Salud.\n"
        "Usa los siguientes fragmentos de contexto recuperados para responder la pregunta.\n"
        "Si no sabes la respuesta, di que no la sabes. Sé claro y preciso.\n\n"
        "Contexto:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

