from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


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
    return ChatResponse(
        session_id=request.session_id,
        reply="我已收到你的问题，请先补充数据库类型、版本、完整报错和连接方式。",
        stage="collecting_info",
    )


@app.post("/summary", response_model=SummaryResponse)
def summary(request: SummaryRequest) -> SummaryResponse:
    return SummaryResponse(
        title="待确认的问题标题",
        summary="当前为 mock 工单摘要，后续阶段会根据聊天记录生成完整内容。",
        status="draft",
    )
