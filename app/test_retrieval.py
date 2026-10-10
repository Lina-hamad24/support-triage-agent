from app.retrieval import build_vector_store


vector_store = build_vector_store()

results = vector_store.similarity_search(
    "How long does a refund take?",
    k=2,
)

for document in results:
    print("\n--- RESULT ---")
    print(document.page_content)