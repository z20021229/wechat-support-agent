from pydantic import BaseModel


class ClassificationResult(BaseModel):
    category: str
    label: str
    confidence: float
    reason: str


CLASSIFICATION_RULES = [
    {
        "category": "service_unavailable",
        "label": "服务不可用",
        "keywords": ["启动失败", "服务不可用", "down", "宕机", "进程不存在", "端口未监听"],
    },
    {
        "category": "database_connection",
        "label": "数据库连接问题",
        "keywords": ["连接", "超时", "timeout", "无法连接", "connection refused", "端口", "监听"],
    },
    {
        "category": "permission_error",
        "label": "权限问题",
        "keywords": ["权限", "permission", "denied", "授权", "grant", "用户无权限"],
    },
    {
        "category": "sql_error",
        "label": "SQL 执行错误",
        "keywords": ["SQL", "语法", "syntax", "ORA", "ERROR", "执行失败", "字段不存在", "表不存在"],
    },
    {
        "category": "performance_issue",
        "label": "性能问题",
        "keywords": ["慢", "卡", "性能", "耗时", "查询慢", "CPU", "内存", "等待"],
    },
]


def classify_issue(message: str) -> ClassificationResult:
    normalized_message = message.lower()

    for rule in CLASSIFICATION_RULES:
        matched_keywords = [
            keyword
            for keyword in rule["keywords"]
            if keyword.lower() in normalized_message
        ]
        if matched_keywords:
            return ClassificationResult(
                category=rule["category"],
                label=rule["label"],
                confidence=0.8,
                reason=f"命中关键词：{'、'.join(matched_keywords)}",
            )

    return ClassificationResult(
        category="other",
        label="其他问题",
        confidence=0.3,
        reason="未命中已知关键词",
    )
