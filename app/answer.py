from langchain_ollama import ChatOllama
from app.retrieval import build_vector_store


llm = ChatOllama(
    model="llama3:latest",
    temperature=0,
)


def answer_question(question: str):
    vector_store = build_vector_store()

    documents = vector_store.similarity_search(
        question,
        k=2,
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are a customer support assistant.

Answer the customer's question using ONLY the information
provided in the context below.

If the answer is not contained in the context, say:
"I don't have enough information to answer that."

Context:
{context}

Customer question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content