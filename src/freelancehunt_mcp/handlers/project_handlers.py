# ================================================
# Обработчики для проектов
# ================================================

from typing import Dict, Any, List
import mcp.types as types

from ..api_client import FreelanceHuntClient
from ..models import SearchFilters
from .base import create_json_response, create_error_response


async def handle_search_projects(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    
    # Build search filters
    filters = SearchFilters(
        skill_id=arguments.get("skill_ids"),
        budget_from=arguments.get("budget_from"),
        budget_to=arguments.get("budget_to"),
        employer_id=arguments.get("employer_id"),
        only_remote=arguments.get("only_remote")
    )
    
    response = await client.search_projects(
        page=page,
        per_page=per_page,
        filters=filters
    )
    
    result = {
        "projects": [project.model_dump() for project in response.data],
        "meta": response.meta,
        "links": response.links
    }
    
    return create_json_response(result)


async def handle_get_project(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    project_id = arguments.get("project_id")
    if not project_id:
        return create_error_response("project_id is required")
    
    project = await client.get_project(project_id)
    return create_json_response(project.model_dump())


async def handle_get_project_bids(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    project_id = arguments.get("project_id")
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    
    if not project_id:
        return create_error_response("project_id is required")
    
    response = await client.get_project_bids(
        project_id=project_id,
        page=page,
        per_page=per_page
    )
    
    result = {
        "bids": [bid.model_dump() for bid in response.data],
        "links": response.links,
        "meta": response.meta
    }
    
    return create_json_response(result)


async def handle_get_project_comments(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    project_id = arguments.get("project_id")
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    
    if not project_id:
        return create_error_response("project_id is required")
    
    response = await client.get_project_comments(
        project_id=project_id,
        page=page,
        per_page=per_page
    )
    
    result = {
        "comments": [comment.model_dump() for comment in response.data],
        "links": response.links
    }
    
    return create_json_response(result)
