from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.agent import build_support_reply
from backend.classifier import ClassificationResult
from backend.session_state import get_or_create_session
from backend.ticket_summary import generate_ticket_summary


SERVICE_NAME = "wechat-support-agent"

app = FastAPI(title=SERVICE_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    stage: str
    classification: ClassificationResult
    knowledge: dict[str, str | bool]
    next_questions: list[str]
    session_state: dict[str, list[str]]


class SummaryRequest(BaseModel):
    session_id: str
    messages: list[Any] = Field(default_factory=list)


class SummaryResponse(BaseModel):
    session_id: str
    title: str
    category: str
    label: str
    problem_description: str
    collected_info: list[str]
    possible_causes: list[str]
    suggested_steps: list[str]
    status: str
    follow_up: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    support_reply = build_support_reply(request.session_id, request.message)
    return ChatResponse(
        session_id=request.session_id,
        **support_reply,
    )


@app.post("/summary", response_model=SummaryResponse)
def summary(request: SummaryRequest) -> SummaryResponse:
    messages = request.messages or get_or_create_session(request.session_id)["messages"]
    return SummaryResponse(**generate_ticket_summary(request.session_id, messages))
