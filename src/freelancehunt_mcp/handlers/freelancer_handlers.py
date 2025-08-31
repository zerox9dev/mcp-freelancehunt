# ================================================
# Обработчики для фрилансеров
# ================================================

from typing import Dict, Any, List
import mcp.types as types

from ..api_client import FreelanceHuntClient
from .base import create_json_response, create_error_response



async def handle_get_freelancer(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    freelancer_id = arguments.get("freelancer_id")
    if not freelancer_id:
        return create_error_response("freelancer_id is required")
    
    freelancer = await client.get_freelancer(freelancer_id)
    return create_json_response(freelancer.model_dump())


async def handle_get_my_profile(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    profile = await client.get_my_profile()
    return create_json_response(profile.model_dump())


async def handle_get_my_bids(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    
    response = await client.get_my_bids(page=page, per_page=per_page)
    
    result = {
        "my_bids": [bid.model_dump() for bid in response.data],
        "links": response.links,
        "meta": response.meta
    }
    
    return create_json_response(result)


async def handle_get_freelancer_portfolio(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    freelancer_id = arguments.get("freelancer_id")
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    
    if not freelancer_id:
        return create_error_response("freelancer_id is required")
    
    response = await client.get_freelancer_portfolio(
        freelancer_id=freelancer_id,
        page=page,
        per_page=per_page
    )
    
    result = {
        "portfolio": [item.model_dump() for item in response.data],
        "links": response.links
    }
    
    return create_json_response(result)


async def handle_get_freelancer_reviews(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    freelancer_id = arguments.get("freelancer_id")
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    
    if not freelancer_id:
        return create_error_response("freelancer_id is required")
    
    reviews = await client.get_freelancer_reviews(
        freelancer_id=freelancer_id,
        page=page,
        per_page=per_page
    )
    
    return create_json_response(reviews)
