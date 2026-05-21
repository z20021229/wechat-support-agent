import re
from typing import Any

from backend.classifier import classify_issue


DATABASE_NAMES = ["GaussDB", "PostgreSQL", "MySQL", "Oracle"]

SUMMARY_RULES = {
    "database_connection": {
        "title": "数据库连接超时问题",
        "problem_description": "客户反馈数据库连接超时或无法连接。",
        "possible_causes": [
            "数据库服务未监听目标端口",
            "防火墙或安全组拦截",
            "连接地址或端口配置错误",
        ],
        "suggested_steps": [
            "确认数据库服务是否正常运行",
            "检查端口监听状态",
            "检查防火墙或安全组策略",
            "确认客户端连接地址和端口配置",
        ],
        "follow_up": [
            "需要客户补充完整报错截图",
            "需要确认服务端监听状态",
        ],
    },
    "permission_error": {
        "title": "权限不足问题",
        "problem_description": "客户反馈执行操作时出现权限不足。",
        "possible_causes": [
            "当前用户缺少目标对象权限",
            "角色未启用或授权未生效",
            "对象所属 schema 或环境选择错误",
        ],
        "suggested_steps": [
            "确认当前用户和执行的操作",
            "检查目标对象权限",
            "确认角色和授权是否生效",
            "按最小权限原则补充授权方案",
        ],
        "follow_up": [
            "需要客户补充当前用户",
            "需要客户补充完整报错和目标对象名称",
        ],
    },
    "sql_error": {
        "title": "SQL 执行错误问题",
        "problem_description": "客户反馈 SQL 执行失败或报错。",
        "possible_causes": [
            "SQL 语法与当前数据库不兼容",
            "字段、表或对象不存在",
            "参数或数据类型不匹配",
        ],
        "suggested_steps": [
            "收集完整 SQL 和完整报错",
            "确认数据库类型和版本",
            "检查表结构、字段名和对象是否存在",
            "将 SQL 简化为最小复现语句",
        ],
        "follow_up": [
            "需要客户补充完整 SQL",
            "需要客户补充完整报错和数据库版本",
        ],
    },
    "performance_issue": {
        "title": "性能问题",
        "problem_description": "客户反馈查询或系统响应较慢。",
        "possible_causes": [
            "缺少索引或执行计划不合理",
            "数据量增长导致查询耗时增加",
            "CPU、内存、IO 或锁等待导致性能下降",
        ],
        "suggested_steps": [
            "收集慢 SQL 和执行耗时",
            "确认数据量和执行计划",
            "检查 CPU、内存、IO 和锁等待情况",
            "对比近期发布、配置或数据量变化",
        ],
        "follow_up": [
            "需要客户补充慢 SQL 和执行耗时",
            "需要客户补充执行计划和资源指标",
        ],
    },
    "service_unavailable": {
        "title": "服务不可用问题",
        "problem_description": "客户反馈服务启动失败或不可用。",
        "possible_causes": [
            "服务进程未启动",
            "端口未监听或被占用",
            "配置错误或依赖服务不可达",
        ],
        "suggested_steps": [
            "确认服务名称和启动命令",
            "检查进程状态",
            "检查端口监听状态",
            "查看最近启动日志摘要",
        ],
        "follow_up": [
            "需要客户补充服务名称和启动命令",
            "需要客户补充日志摘要和端口监听状态",
        ],
    },
    "other": {
        "title": "待确认的问题标题",
        "problem_description": "当前问题信息不足，需要继续收集背景和环境信息。",
        "possible_causes": [
            "问题背景信息不足",
            "操作步骤或环境信息缺失",
            "需要进一步判断问题类型",
        ],
        "suggested_steps": [
            "补充问题背景",
            "补充操作步骤和完整报错",
            "确认环境信息和影响范围",
        ],
        "follow_up": [
            "需要客户补充问题背景",
            "需要客户补充完整报错和环境信息",
        ],
    },
}


def _user_contents(messages: list[Any]) -> list[str]:
    contents = []
    for message in messages:
        if isinstance(message, dict) and message.get("role") == "user":
            content = str(message.get("content", "")).strip()
            if content:
                contents.append(content)
    return contents


def _detect_database_type(text: str) -> str | None:
    lower_text = text.lower()
    for database_name in DATABASE_NAMES:
        if database_name.lower() in lower_text:
            return database_name
    return None


def _collect_info(text: str) -> list[str]:
    collected_info = []

    database_type = _detect_database_type(text)
    if database_type:
        collected_info.append(f"数据库类型：{database_type}")

    port_match = re.search(r"(?:端口|port)\s*[:：]?\s*(\d{2,5})", text, re.IGNORECASE)
    if port_match:
        collected_info.append(f"端口：{port_match.group(1)}")

    if "telnet" in text.lower():
        status = "不通" if any(keyword in text for keyword in ["不通", "失败", "超时"]) else "已提供"
        collected_info.append(f"telnet 检查：{status}")

    if "ping" in text.lower():
        status = "不通" if any(keyword in text for keyword in ["不通", "失败", "超时"]) else "已提供"
        collected_info.append(f"ping 检查：{status}")

    keyword_checks = [
        ("权限", "权限相关报错已提供"),
        ("SQL", "SQL 相关信息已提供"),
        ("ORA", "ORA 错误码已提供"),
        ("ERROR", "ERROR 报错已提供"),
        ("timeout", "timeout 报错已提供"),
    ]
    for keyword, description in keyword_checks:
        if keyword.lower() in text.lower() and description not in collected_info:
            collected_info.append(description)

    return collected_info


def generate_ticket_summary(session_id: str, messages: list[Any]) -> dict[str, Any]:
    user_contents = _user_contents(messages)
    combined_text = " ".join(user_contents)
    classification = classify_issue(combined_text) if combined_text else classify_issue("")
    rules = SUMMARY_RULES[classification.category]
    collected_info = _collect_info(combined_text)

    follow_up = list(rules["follow_up"])
    if not user_contents:
        follow_up.insert(0, "需要客户补充问题描述")
    if not collected_info:
        collected_info = ["当前已收集信息不足"]

    return {
        "session_id": session_id,
        "title": rules["title"],
        "category": classification.category,
        "label": classification.label,
        "problem_description": rules["problem_description"],
        "collected_info": collected_info,
        "possible_causes": rules["possible_causes"],
        "suggested_steps": rules["suggested_steps"],
        "status": "draft",
        "follow_up": follow_up,
    }
