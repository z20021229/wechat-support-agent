from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.agent import build_support_reply
from backend.classifier import ClassificationResult


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


class SummaryRequest(BaseModel):
    session_id: str
    messages: list[Any] = Field(default_factory=list)


class SummaryResponse(BaseModel):
    title: str
    summary: str
    status: str


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    support_reply = build_support_reply(request.message)
    return ChatResponse(
        session_id=request.session_id,
        **support_reply,
    )


@app.post("/summary", response_model=SummaryResponse)
def summary(request: SummaryRequest) -> SummaryResponse:
    return SummaryResponse(
        title="待确认的问题标题",
        summary="当前为 mock 工单摘要，后续阶段会根据聊天记录生成完整内容。",
        status="draft",
    )
