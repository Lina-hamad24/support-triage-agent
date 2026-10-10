from app.graph import graph


questions = [
    "How long does a refund take?",
    "My order is late",
    "My account is locked",
]

for question in questions:
    result = graph.invoke({
        "question": question,
        "decision": "",
        "answer": "",
        "order_number": "",
    })

    print("\nQUESTION:", question)
    print("DECISION:", result["decision"])
    print("ANSWER:", result["answer"])