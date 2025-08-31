

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional, Sequence

from dotenv import load_dotenv
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from .api_client import FreelanceHuntClient, FreelanceHuntAPIError
from .models import SearchFilters

# Load environment variables
load_dotenv()

# Initialize the MCP server
server = Server("freelancehunt-mcp")

# Global client instance
client: Optional[FreelanceHuntClient] = None


def init_client():
    global client
    try:
        client = FreelanceHuntClient()
        print("FreelanceHunt MCP Server initialized successfully", file=sys.stderr)
    except ValueError as e:
        print(f"Warning: FreelanceHunt client not initialized: {e}", file=sys.stderr)
        print("Please set FREELANCEHUNT_API_KEY environment variable", file=sys.stderr)
        # Don't exit, allow server to start without API key for testing
        client = None


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="search_projects",
            description="Search for projects on FreelanceHunt with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number (default: 1)",
                        "minimum": 1
                    },
                    "per_page": {
                        "type": "integer", 
                        "description": "Items per page (default: 20, max: 50)",
                        "minimum": 1,
                        "maximum": 50
                    },
                    "skill_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of skill IDs to filter by"
                    },
                    "budget_from": {
                        "type": "number",
                        "description": "Minimum budget"
                    },
                    "budget_to": {
                        "type": "number", 
                        "description": "Maximum budget"
                    },
                    "employer_id": {
                        "type": "integer",
                        "description": "Filter by employer ID"
                    },
                    "only_remote": {
                        "type": "boolean",
                        "description": "Show only remote projects"
                    }
                }
            }
        ),
        types.Tool(
            name="get_project",
            description="Get detailed information about a specific project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Project ID",
                        "minimum": 1
                    }
                },
                "required": ["project_id"]
            }
        ),
        types.Tool(
            name="search_freelancers",
            description="Search for freelancers on FreelanceHunt",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number (default: 1)",
                        "minimum": 1
                    },
                    "per_page": {
                        "type": "integer",
                        "description": "Items per page (default: 20, max: 50)",
                        "minimum": 1,
                        "maximum": 50
                    },
                    "skill_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of skill IDs to filter by"
                    },
                    "location_id": {
                        "type": "integer",
                        "description": "Filter by location ID"
                    }
                }
            }
        ),
        types.Tool(
            name="get_freelancer",
            description="Get detailed information about a specific freelancer",
            inputSchema={
                "type": "object",
                "properties": {
                    "freelancer_id": {
                        "type": "integer",
                        "description": "Freelancer ID",
                        "minimum": 1
                    }
                },
                "required": ["freelancer_id"]
            }
        ),
        types.Tool(
            name="get_skills",
            description="Get list of available skills on FreelanceHunt",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="get_locations",
            description="Get list of available locations on FreelanceHunt",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="get_threads",
            description="Get list of threads (conversations) on FreelanceHunt",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "Page number (default: 1)",
                        "minimum": 1
                    },
                    "per_page": {
                        "type": "integer",
                        "description": "Items per page (default: 20, max: 50)",
                        "minimum": 1,
                        "maximum": 50
                    }
                }
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any]
) -> List[types.TextContent]:
    if not client:
        return [types.TextContent(
            type="text",
            text="Error: FreelanceHunt client not initialized. Please set FREELANCEHUNT_API_KEY environment variable and restart the server."
        )]
    
    try:
        if name == "search_projects":
            return await handle_search_projects(arguments)
        elif name == "get_project":
            return await handle_get_project(arguments)
        elif name == "search_freelancers":
            return await handle_search_freelancers(arguments)
        elif name == "get_freelancer":
            return await handle_get_freelancer(arguments)
        elif name == "get_skills":
            return await handle_get_skills(arguments)
        elif name == "get_locations":
            return await handle_get_locations(arguments)
        elif name == "get_threads":
            return await handle_get_threads(arguments)
        else:
            return [types.TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]
    except FreelanceHuntAPIError as e:
        return [types.TextContent(
            type="text",
            text=f"FreelanceHunt API Error: {e}"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Unexpected error: {e}"
        )]


async def handle_search_projects(arguments: Dict[str, Any]) -> List[types.TextContent]:
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
    
    # Format response
    result = {
        "projects": [project.model_dump() for project in response.data],
        "meta": response.meta,
        "links": response.links
    }
    
    return [types.TextContent(
        type="text",
        text=json.dumps(result, indent=2, default=str, ensure_ascii=False)
    )]


async def handle_get_project(arguments: Dict[str, Any]) -> List[types.TextContent]:
    project_id = arguments.get("project_id")
    if not project_id:
        return [types.TextContent(
            type="text",
            text="Error: project_id is required"
        )]
    
    project = await client.get_project(project_id)
    
    return [types.TextContent(
        type="text",
        text=json.dumps(project.model_dump(), indent=2, default=str, ensure_ascii=False)
    )]


async def handle_search_freelancers(arguments: Dict[str, Any]) -> List[types.TextContent]:
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    skill_ids = arguments.get("skill_ids")
    location_id = arguments.get("location_id")
    
    freelancers = await client.search_freelancers(
        page=page,
        per_page=per_page,
        skill_ids=skill_ids,
        location_id=location_id
    )
    
    result = [freelancer.model_dump() for freelancer in freelancers]
    
    return [types.TextContent(
        type="text",
        text=json.dumps(result, indent=2, default=str, ensure_ascii=False)
    )]


async def handle_get_freelancer(arguments: Dict[str, Any]) -> List[types.TextContent]:
    freelancer_id = arguments.get("freelancer_id")
    if not freelancer_id:
        return [types.TextContent(
            type="text",
            text="Error: freelancer_id is required"
        )]
    
    freelancer = await client.get_freelancer(freelancer_id)
    
    return [types.TextContent(
        type="text",
        text=json.dumps(freelancer.model_dump(), indent=2, default=str, ensure_ascii=False)
    )]


async def handle_get_skills(arguments: Dict[str, Any]) -> List[types.TextContent]:
    skills = await client.get_skills()
    
    return [types.TextContent(
        type="text",
        text=json.dumps(skills, indent=2, default=str, ensure_ascii=False)
    )]


async def handle_get_locations(arguments: Dict[str, Any]) -> List[types.TextContent]:
    locations = await client.get_locations()
    
    return [types.TextContent(
        type="text",
        text=json.dumps(locations, indent=2, default=str, ensure_ascii=False)
    )]


async def handle_get_threads(arguments: Dict[str, Any]) -> List[types.TextContent]:
    page = arguments.get("page", 1)
    per_page = arguments.get("per_page", 20)
    
    response = await client.get_threads(page=page, per_page=per_page)
    
    # Format response
    result = {
        "threads": [thread.model_dump() for thread in response.data],
        "meta": response.meta,
        "links": response.links
    }
    
    return [types.TextContent(
        type="text",
        text=json.dumps(result, indent=2, default=str, ensure_ascii=False)
    )]


async def run_server():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            InitializationOptions(
                server_name="freelancehunt-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def main():
    # Initialize the client
    init_client()
    
    # Run the server
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
