# ================================================
# Обработчики для конкурсов
# ================================================

from typing import Dict, Any, List
import mcp.types as types

from ..api_client import FreelanceHuntClient
from .base import create_json_response, create_error_response


async def handle_search_contests(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    skill_ids = arguments.get("skill_ids")
    
    response = await client.search_contests(
        page=page,
        per_page=per_page,
        skill_ids=skill_ids
    )
    
    result = {
        "contests": [contest.model_dump() for contest in response.data],
        "links": response.links,
        "meta": response.meta
    }
    
    return create_json_response(result)


async def handle_get_contest(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    contest_id = arguments.get("contest_id")
    
    if not contest_id:
        return create_error_response("contest_id is required")
    
    contest = await client.get_contest(contest_id)
    return create_json_response(contest.model_dump())
