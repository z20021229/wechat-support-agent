from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]

KNOWLEDGE_FILES = {
    "database_connection": "knowledge/database_connection.md",
    "permission_error": "knowledge/permission_error.md",
    "sql_error": "knowledge/sql_error.md",
    "performance_issue": "knowledge/performance_issue.md",
    "service_unavailable": "knowledge/service_unavailable.md",
    "other": "knowledge/other_issue.md",
}


def load_knowledge(category: str) -> dict[str, Any]:
    resolved_category = category if category in KNOWLEDGE_FILES else "other"
    relative_file = KNOWLEDGE_FILES[resolved_category]
    path = REPO_ROOT / relative_file

    return {
        "category": resolved_category,
        "file": relative_file,
        "available": path.exists(),
        "content": path.read_text(encoding="utf-8") if path.exists() else "",
    }
