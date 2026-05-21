from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.classifier import ClassificationResult, classify_issue


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


class SummaryRequest(BaseModel):
    session_id: str
    messages: list[Any] = Field(default_factory=list)


class SummaryResponse(BaseModel):
    title: str
    summary: str
    status: str


FOLLOW_UP_REPLIES = {
    "database_connection": "请补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 结果。",
    "permission_error": "请补充当前用户、执行的操作、完整报错，以及相关对象权限信息。",
    "sql_error": "请补充完整 SQL、完整报错、数据库类型和版本。",
    "performance_issue": "请补充慢 SQL、执行耗时、数据量、执行计划和系统资源情况。",
    "service_unavailable": "请补充服务名称、启动命令、日志、端口监听和进程状态。",
    "other": "请补充问题背景、操作步骤、完整报错和环境信息。",
}


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    classification = classify_issue(request.message)
    return ChatResponse(
        session_id=request.session_id,
        reply=FOLLOW_UP_REPLIES[classification.category],
        stage="collecting_info",
        classification=classification,
    )


@app.post("/summary", response_model=SummaryResponse)
def summary(request: SummaryRequest) -> SummaryResponse:
    return SummaryResponse(
        title="待确认的问题标题",
        summary="当前为 mock 工单摘要，后续阶段会根据聊天记录生成完整内容。",
        status="draft",
    )
