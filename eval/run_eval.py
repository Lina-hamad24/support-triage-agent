import json

from app.graph import graph


def load_cases():
    with open("eval/cases.json", "r", encoding="utf-8") as file:
        return json.load(file)


def run_evaluation():
    cases = load_cases()

    total = len(cases)
    correct = 0

    for case in cases:
        result = graph.invoke({
            "question": case["question"],
            "decision": "",
            "answer": "",
            "order_number": "",
        })

        predicted = result["decision"]
        expected = case["expected_decision"]

        is_correct = predicted == expected

        if is_correct:
            correct += 1

        print("\nQuestion:", case["question"])
        print("Expected:", expected)
        print("Predicted:", predicted)
        print("Result:", "PASS" if is_correct else "FAIL")

    accuracy = correct / total * 100

    print("\n====================")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Passed: {correct}/{total}")
    print("====================")


if __name__ == "__main__":
    run_evaluation()