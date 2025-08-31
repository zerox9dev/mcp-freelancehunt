# ================================================
# Базовые утилиты для обработчиков
# ================================================

import json
from typing import Dict, Any, List
import mcp.types as types


def create_json_response(data: Any) -> List[types.TextContent]:
    """Создает стандартный JSON ответ для MCP"""
    return [types.TextContent(
        type="text",
        text=json.dumps(data, indent=2, default=str, ensure_ascii=False)
    )]


def create_error_response(message: str) -> List[types.TextContent]:
    """Создает ответ с ошибкой"""
    return [types.TextContent(
        type="text",
        text=f"Error: {message}"
    )]
