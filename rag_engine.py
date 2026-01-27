import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

def inicializar_asistente_monteverde():
    # 1. Configuración de rutas (compatibles con Docker)
    pdf_path = "articulo_monteverde.pdf"
    persist_directory = "/app/chroma_db" if os.path.exists("/app") else "chroma_db"

    # 2. Carga y fragmentación del documento
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Vector Store y Embeddings
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 4. Configuración del Modelo (Claude 3.5 via LangChain)
    # Nota: Asegúrate de tener instalada langchain-anthropic si prefieres Claude directamente
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    # 5. Definición del Prompt
    system_prompt = (
        "Eres un asistente experto en la teoría de 'The Great Corruption' del Ph.D. Vicente Humberto Monteverde. "
        "Usa los siguientes fragmentos de contexto recuperado para responder la pregunta. "
        "Si no sabes la respuesta, di que no lo sabes. "
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # 6. Creación de la Cadena RAG (Sintaxis 0.3.x)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain