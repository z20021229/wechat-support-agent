import re
from typing import Any

from backend.classifier import classify_issue


SESSION_STORE: dict[str, dict[str, Any]] = {}

REQUIRED_INFO = {
    "database_connection": ["数据库类型", "数据库版本", "连接地址", "端口", "完整报错", "ping 结果", "telnet 结果"],
    "permission_error": ["当前用户", "执行操作", "SQL", "对象名", "完整报错", "授权情况"],
    "sql_error": ["SQL", "完整报错", "数据库类型", "数据库版本", "表结构", "对象名"],
    "performance_issue": ["慢 SQL", "执行耗时", "数据量", "执行计划", "CPU", "内存", "IO", "锁等待"],
    "service_unavailable": ["服务名称", "启动命令", "进程状态", "端口监听", "日志", "最近变更"],
    "other": ["问题背景", "操作步骤", "完整报错", "环境信息", "影响范围"],
}


def _new_session(session_id: str) -> dict[str, Any]:
    return {
        "session_id": session_id,
        "category": "other",
        "collected_info": [],
        "missing_info": REQUIRED_INFO["other"].copy(),
        "latest_user_message": "",
        "messages": [],
    }


def reset_sessions() -> None:
    SESSION_STORE.clear()


def reset_session(session_id: str) -> None:
    SESSION_STORE.pop(session_id, None)


def get_or_create_session(session_id: str) -> dict[str, Any]:
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = _new_session(session_id)
    return SESSION_STORE[session_id]


def _add_collected_info(session: dict[str, Any], item: str) -> None:
    if item not in session["collected_info"]:
        session["collected_info"].append(item)


def _detect_database_type(content: str) -> str | None:
    for database_name in ["GaussDB", "PostgreSQL", "MySQL", "Oracle"]:
        if database_name.lower() in content.lower():
            return database_name
    return None


def _extract_common_info(session: dict[str, Any], content: str) -> None:
    database_type = _detect_database_type(content)
    if database_type:
        _add_collected_info(session, f"数据库类型：{database_type}")

    port_match = re.search(r"(?:端口|port)\s*[:：]?\s*(\d{2,5})", content, re.IGNORECASE)
    if port_match:
        _add_collected_info(session, f"端口：{port_match.group(1)}")

    if "telnet" in content.lower():
        status = "不通" if any(keyword in content for keyword in ["不通", "失败", "超时"]) else "已提供"
        _add_collected_info(session, f"telnet 结果：{status}")

    if "ping" in content.lower():
        status = "不通" if any(keyword in content for keyword in ["不通", "失败", "超时"]) else "已提供"
        _add_collected_info(session, f"ping 结果：{status}")

    if any(keyword in content for keyword in ["报错", "ERROR", "ORA", "denied", "权限不足", "表不存在"]):
        _add_collected_info(session, "完整报错：已提供")

    if "SQL" in content.upper():
        _add_collected_info(session, "SQL：已提供")


def _extract_category_info(session: dict[str, Any], content: str) -> None:
    if any(keyword in content for keyword in ["地址", "host", "连接串"]):
        _add_collected_info(session, "连接地址：已提供")
    if any(keyword in content for keyword in ["版本", "version"]):
        _add_collected_info(session, "数据库版本：已提供")
    if any(keyword in content for keyword in ["用户", "账号"]):
        _add_collected_info(session, "当前用户：已提供")
    if any(keyword in content for keyword in ["执行", "操作"]):
        _add_collected_info(session, "执行操作：已提供")
    if any(keyword in content for keyword in ["对象", "表", "字段"]):
        _add_collected_info(session, "对象名：已提供")
    if any(keyword in content for keyword in ["授权", "grant", "权限"]):
        _add_collected_info(session, "授权情况：已提供")
    if "表结构" in content:
        _add_collected_info(session, "表结构：已提供")
    if any(keyword in content for keyword in ["慢 SQL", "慢SQL"]):
        _add_collected_info(session, "慢 SQL：已提供")
    if any(keyword in content for keyword in ["耗时", "秒", "ms"]):
        _add_collected_info(session, "执行耗时：已提供")
    if any(keyword in content for keyword in ["数据量", "行数"]):
        _add_collected_info(session, "数据量：已提供")
    if "执行计划" in content:
        _add_collected_info(session, "执行计划：已提供")
    if "CPU" in content.upper():
        _add_collected_info(session, "CPU：已提供")
    if "内存" in content:
        _add_collected_info(session, "内存：已提供")
    if "IO" in content.upper():
        _add_collected_info(session, "IO：已提供")
    if "锁" in content:
        _add_collected_info(session, "锁等待：已提供")
    if "服务" in content:
        _add_collected_info(session, "服务名称：已提供")
    if any(keyword in content for keyword in ["启动命令", "命令"]):
        _add_collected_info(session, "启动命令：已提供")
    if any(keyword in content for keyword in ["进程", "ps "]):
        _add_collected_info(session, "进程状态：已提供")
    if any(keyword in content for keyword in ["监听", "端口未监听"]):
        _add_collected_info(session, "端口监听：已提供")
    if "日志" in content:
        _add_collected_info(session, "日志：已提供")
    if any(keyword in content for keyword in ["变更", "发布"]):
        _add_collected_info(session, "最近变更：已提供")


def _collected_key(item: str) -> str:
    return item.split("：", 1)[0]


def _update_missing_info(session: dict[str, Any]) -> None:
    required = REQUIRED_INFO.get(session["category"], REQUIRED_INFO["other"])
    collected_keys = {_collected_key(item) for item in session["collected_info"]}
    session["missing_info"] = [item for item in required if item not in collected_keys]


def update_session_with_message(session_id: str, role: str, content: str) -> dict[str, Any]:
    session = get_or_create_session(session_id)
    session["messages"].append({"role": role, "content": content})

    if role == "user":
        session["latest_user_message"] = content
        classification = classify_issue(content)
        if classification.category != "other" or session["category"] == "other":
            session["category"] = classification.category
        _extract_common_info(session, content)
        _extract_category_info(session, content)
        _update_missing_info(session)

    return session
