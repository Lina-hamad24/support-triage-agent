from typing import TypedDict

from langgraph.graph import StateGraph, END

from app.answer import answer_question
from app.tickets import create_ticket
from app.config import logger


class AgentState(TypedDict):
    question: str
    decision: str
    answer: str
    order_number: str


def decide(state: AgentState):
    question = state["question"].lower().strip()
    order_number = state.get("order_number", "").strip()

    # 1. Escalate account/security problems
    escalation_keywords = [
        "locked",
        "lock",
        "cannot access my account",
        "can't access my account",
        "account access",
        "security issue",
    ]

    if any(keyword in question for keyword in escalation_keywords):
        decision = "escalate"

    # 2. Clarify order-related requests when the order number is missing
    elif "order" in question:
        clarification_keywords = [
            "late",
            "missing",
            "lost",
            "where is",
            "delayed",
            "forgot",
            "don't know",
            "do not know",
        ]

        if not order_number and any(
            keyword in question
            for keyword in clarification_keywords
        ):
            decision = "clarify"
        else:
            decision = "answer"

    # 3. Otherwise use the RAG answer path
    else:
        decision = "answer"

    # Log the agent's routing decision
    logger.info(
        "Decision | question='%s' | decision='%s'",
        state["question"],
        decision,
    )

    return {
        "decision": decision
    }


def answer(state: AgentState):
    response = answer_question(state["question"])

    return {
        "answer": response
    }


def clarify(state: AgentState):
    return {
        "answer": "Could you please provide your order number?"
    }


def escalate(state: AgentState):
    ticket_id = create_ticket(state["question"])

    return {
        "answer": (
            "Your request has been escalated to our support team. "
            f"Ticket ID: {ticket_id}"
        )
    }


def route(state: AgentState):
    return state["decision"]


graph_builder = StateGraph(AgentState)

graph_builder.add_node("decide", decide)
graph_builder.add_node("answer", answer)
graph_builder.add_node("clarify", clarify)
graph_builder.add_node("escalate", escalate)

graph_builder.set_entry_point("decide")

graph_builder.add_conditional_edges(
    "decide",
    route,
    {
        "answer": "answer",
        "clarify": "clarify",
        "escalate": "escalate",
    },
)

graph_builder.add_edge("answer", END)
graph_builder.add_edge("clarify", END)
graph_builder.add_edge("escalate", END)

graph = graph_builder.compile()