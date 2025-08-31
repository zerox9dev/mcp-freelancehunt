# ================================================
# Обработчики для локаций и справочной информации
# ================================================

from typing import Dict, Any, List
import mcp.types as types

from ..api_client import FreelanceHuntClient
from .base import create_json_response


async def handle_get_skills(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    skills = await client.get_skills()
    return create_json_response(skills)


async def handle_get_locations(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    locations = await client.get_locations()
    return create_json_response(locations)


async def handle_get_countries(client: FreelanceHuntClient, arguments: Dict[str, Any]) -> List[types.TextContent]:
    response = await client.get_countries()
    
    result = {
        "countries": [country.model_dump() for country in response.data],
        "links": response.links
    }
    
    return create_json_response(result)
