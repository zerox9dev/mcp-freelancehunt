# ================================================
# Обработчики для проектов
# ================================================

from typing import Dict, Any, List
import mcp.types as types

from ..api_client import FreelanceHuntClient
from ..models import SearchFilters
from ..models.bid import CreateBidRequest
from ..models.base import ProjectBudget
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
    is_winner = arguments.get("is_winner")
    status = arguments.get("status")
    
    if not project_id:
        return create_error_response("project_id is required")
    
    response = await client.get_project_bids(
        project_id=project_id,
        page=page,
        per_page=per_page,
        is_winner=is_winner,
        status=status
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


async def handle_create_bid(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Создать ставку на проект"""
    project_id = arguments.get("project_id")
    if not project_id:
        return create_error_response("project_id is required")
    
    # Валидация обязательных полей
    required_fields = ["days", "budget", "comment"]
    for field in required_fields:
        if field not in arguments:
            return create_error_response(f"{field} is required")
    
    try:
        # Создание объекта бюджета
        budget_data = arguments["budget"]
        if not isinstance(budget_data, dict) or "amount" not in budget_data or "currency" not in budget_data:
            return create_error_response("budget must be object with amount and currency")
        
        budget = ProjectBudget(amount=budget_data["amount"], currency=budget_data["currency"])
        
        # Создание запроса ставки
        bid_request = CreateBidRequest(
            days=arguments["days"],
            budget=budget,
            comment=arguments["comment"],
            safe_type=arguments.get("safe_type"),
            is_hidden=arguments.get("is_hidden", False)
        )
        
        # Отправка ставки
        response = await client.create_bid(project_id, bid_request)
        
        return create_json_response({
            "message": "Bid created successfully",
            "bid": response
        })
        
    except Exception as e:
        return create_error_response(f"Failed to create bid: {str(e)}")
