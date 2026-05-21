from typing import Any

from backend.classifier import classify_issue
from backend.knowledge_base import load_knowledge
from backend.session_state import update_session_with_message


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

QUESTION_BY_INFO = {
    "数据库类型": "数据库类型是什么？",
    "数据库版本": "数据库版本是什么？",
    "连接地址": "连接地址是什么？",
    "端口": "端口是什么？",
    "完整报错": "完整报错信息是什么？",
    "ping 结果": "ping 检查结果是什么？",
    "telnet 结果": "telnet 检查结果是什么？",
    "当前用户": "当前用户是什么？",
    "执行操作": "执行了什么操作？",
    "SQL": "执行的 SQL 是什么？",
    "对象名": "相关对象名是什么？",
    "授权情况": "当前授权情况是什么？",
    "表结构": "相关表结构是什么？",
    "慢 SQL": "慢 SQL 是什么？",
    "执行耗时": "执行耗时是多少？",
    "数据量": "涉及的数据量是多少？",
    "执行计划": "执行计划是什么？",
    "CPU": "CPU 使用情况如何？",
    "内存": "内存使用情况如何？",
    "IO": "IO 使用情况如何？",
    "锁等待": "是否存在锁等待？",
    "服务名称": "服务名称是什么？",
    "启动命令": "启动命令是什么？",
    "进程状态": "进程状态如何？",
    "端口监听": "端口监听状态如何？",
    "日志": "最近日志摘要是什么？",
    "最近变更": "最近是否有发布或配置变更？",
    "问题背景": "问题背景是什么？",
    "操作步骤": "具体操作步骤是什么？",
    "环境信息": "环境信息是什么？",
    "影响范围": "影响范围是什么？",
}


def _build_dynamic_questions(missing_info: list[str], fallback_category: str) -> list[str]:
    if "数据库类型" in missing_info and "数据库版本" in missing_info:
        remaining_info = [item for item in missing_info if item not in {"数据库类型", "数据库版本"}]
        questions = ["数据库类型和版本是什么？"]
        questions.extend(QUESTION_BY_INFO[item] for item in remaining_info if item in QUESTION_BY_INFO)
        return questions[:4]

    questions = [QUESTION_BY_INFO[item] for item in missing_info if item in QUESTION_BY_INFO]
    return questions[:4] or NEXT_QUESTIONS[fallback_category]


def _build_session_reply(label: str, collected_info: list[str], missing_info: list[str], fallback_reply: str) -> str:
    if not collected_info:
        return fallback_reply

    collected_text = "、".join(collected_info[:4])
    if missing_info:
        missing_text = "、".join(missing_info[:6])
        return f"我判断这可能是{label}。你已经提供了{collected_text}，还需要补充{missing_text}。"

    return f"我判断这可能是{label}。当前关键信息已基本收集，可以继续生成工单摘要或进入人工排查。"


def build_support_reply(session_id: str, message: str) -> dict[str, Any]:
    classification = classify_issue(message)
    knowledge = load_knowledge(classification.category)
    session = update_session_with_message(session_id, "user", message)
    next_questions = _build_dynamic_questions(session["missing_info"], classification.category)

    return {
        "reply": _build_session_reply(
            classification.label,
            session["collected_info"],
            session["missing_info"],
            FOLLOW_UP_REPLIES[classification.category],
        ),
        "stage": "collecting_info",
        "classification": classification.model_dump(),
        "knowledge": {
            "file": knowledge["file"],
            "available": knowledge["available"],
        },
        "next_questions": next_questions,
        "session_state": {
            "collected_info": session["collected_info"],
            "missing_info": session["missing_info"],
        },
    }
