from fastapi import FastAPI
from pydantic import BaseModel

from app.graph import graph


app = FastAPI(
    title="Support Triage Agent",
    description="AI-powered customer support agent using RAG and LangGraph",
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    decision: str


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):

    result = graph.invoke({
        "question": request.question,
        "decision": "",
        "answer": "",
    })

    return AnswerResponse(
        answer=result["answer"],
        decision=result["decision"],
    )