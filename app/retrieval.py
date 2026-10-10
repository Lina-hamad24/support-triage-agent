from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


FAQ_DIR = Path("data/faq")


def build_vector_store():
    loader = DirectoryLoader(
        str(FAQ_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
    )

    documents = loader.load()

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )

    return vector_store