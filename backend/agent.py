from typing import Any

from backend.classifier import classify_issue
from backend.knowledge_base import load_knowledge


FOLLOW_UP_REPLIES = {
    "database_connection": "我判断这可能是数据库连接问题。请先补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 检查结果。",
    "permission_error": "我判断这可能是权限问题。请先补充当前用户、执行的操作、完整报错，以及相关对象权限信息。",
    "sql_error": "我判断这可能是 SQL 执行错误。请先补充完整 SQL、完整报错、数据库类型和版本。",
    "performance_issue": "我判断这可能是性能问题。请先补充慢 SQL、执行耗时、数据量、执行计划和系统资源情况。",
    "service_unavailable": "我判断这可能是服务不可用问题。请先补充服务名称、启动命令、日志、端口监听和进程状态。",
    "other": "我还需要更多信息来判断问题类型。请先补充问题背景、操作步骤、完整报错和环境信息。",
}

NEXT_QUESTIONS = {
    "database_connection": [
        "数据库类型和版本是什么？",
        "连接地址和端口是什么？",
        "完整报错信息是什么？",
        "ping 和 telnet 检查结果是什么？",
    ],
    "permission_error": [
        "当前用户是什么？",
        "执行了什么 SQL 或操作？",
        "完整报错信息是什么？",
        "相关对象权限信息是什么？",
    ],
    "sql_error": [
        "完整 SQL 是什么？",
        "完整报错信息是什么？",
        "数据库类型和版本是什么？",
        "相关表结构和字段名是什么？",
    ],
    "performance_issue": [
        "慢 SQL 或慢操作是什么？",
        "执行耗时和发生频率是多少？",
        "数据量和执行计划是什么？",
        "CPU、内存、IO 或锁等待情况如何？",
    ],
    "service_unavailable": [
        "服务名称是什么？",
        "启动命令和启动用户是什么？",
        "最近日志摘要是什么？",
        "端口监听和进程状态如何？",
    ],
    "other": [
        "问题背景是什么？",
        "具体操作步骤是什么？",
        "完整报错信息是什么？",
        "环境信息和影响范围是什么？",
    ],
}


def build_support_reply(message: str) -> dict[str, Any]:
    classification = classify_issue(message)
    knowledge = load_knowledge(classification.category)

    return {
        "reply": FOLLOW_UP_REPLIES[classification.category],
        "stage": "collecting_info",
        "classification": classification.model_dump(),
        "knowledge": {
            "file": knowledge["file"],
            "available": knowledge["available"],
        },
        "next_questions": NEXT_QUESTIONS[classification.category],
    }
