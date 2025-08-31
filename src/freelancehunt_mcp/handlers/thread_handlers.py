# ================================================
# Обработчики для тредов и сообщений
# ================================================

from typing import Dict, Any, List
import mcp.types as types

from ..api_client import FreelanceHuntClient
from .base import create_json_response


async def handle_get_threads(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    
    response = await client.get_threads(page=page, per_page=per_page)
    
    result = {
        "threads": [thread.model_dump() for thread in response.data],
        "meta": response.meta,
        "links": response.links
    }
    
    return create_json_response(result)
