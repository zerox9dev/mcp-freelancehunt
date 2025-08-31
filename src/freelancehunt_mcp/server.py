# ================================================
# MCP Server для FreelanceHunt API
# ================================================

import asyncio
import sys
from typing import Any, Dict, List, Optional, Sequence

from dotenv import load_dotenv
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from .api_client import FreelanceHuntClient, FreelanceHuntAPIError
from .handlers import (
    handle_search_projects,
    handle_get_project,
    handle_get_project_bids,
    handle_get_project_comments,
    handle_get_freelancer,
    handle_get_my_profile,
    handle_get_my_bids,
    handle_get_freelancer_portfolio,
    handle_get_freelancer_reviews,
    handle_search_contests,
    handle_get_contest,
    handle_get_threads,
    handle_get_skills,

    handle_get_countries,
    handle_get_cities
)

# ================================================
# Инициализация
# ================================================

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
        client = None


# ================================================
# Конфигурация tools
# ================================================

TOOLS_CONFIG = [
    {
        "name": "search_projects",
        "description": "Search for projects on FreelanceHunt with optional filters",
        "schema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "Page number (default: 1)", "minimum": 1},
                "per_page": {"type": "integer", "description": "Items per page (default: 20, max: 50)", "minimum": 1, "maximum": 50},
                "skill_ids": {"type": "array", "items": {"type": "integer"}, "description": "List of skill IDs to filter by"},
                "budget_from": {"type": "number", "description": "Minimum budget"},
                "budget_to": {"type": "number", "description": "Maximum budget"},
                "employer_id": {"type": "integer", "description": "Filter by employer ID"},
                "only_remote": {"type": "boolean", "description": "Show only remote projects"}
            }
        }
    },
    {
        "name": "get_project",
        "description": "Get detailed information about a specific project",
        "schema": {
            "type": "object",
            "properties": {"project_id": {"type": "integer", "description": "Project ID", "minimum": 1}},
            "required": ["project_id"]
        }
    },

    {
        "name": "get_freelancer",
        "description": "Get detailed information about a specific freelancer",
        "schema": {
            "type": "object",
            "properties": {"freelancer_id": {"type": "integer", "description": "Freelancer ID", "minimum": 1}},
            "required": ["freelancer_id"]
        }
    },
    {
        "name": "get_skills",
        "description": "Get list of available skills on FreelanceHunt",
        "schema": {"type": "object", "properties": {}}
    },

    {
        "name": "get_threads",
        "description": "Get list of threads (conversations) on FreelanceHunt",
        "schema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "Page number (default: 1)", "minimum": 1},
                "per_page": {"type": "integer", "description": "Items per page (default: 20, max: 50)", "minimum": 1, "maximum": 50}
            }
        }
    },
    {
        "name": "get_project_bids",
        "description": "Get bids for a specific project",
        "schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID", "minimum": 1},
                "page": {"type": "integer", "description": "Page number (default: 1)", "minimum": 1},
                "per_page": {"type": "integer", "description": "Items per page (default: 20, max: 50)", "minimum": 1, "maximum": 50}
            },
            "required": ["project_id"]
        }
    },
    {
        "name": "get_project_comments",
        "description": "Get comments for a specific project",
        "schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Project ID", "minimum": 1},
                "page": {"type": "integer", "description": "Page number (default: 1)", "minimum": 1},
                "per_page": {"type": "integer", "description": "Items per page (default: 20, max: 50)", "minimum": 1, "maximum": 50}
            },
            "required": ["project_id"]
        }
    },
    {
        "name": "get_my_bids",
        "description": "Get my bids on FreelanceHunt",
        "schema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "Page number (default: 1)", "minimum": 1},
                "per_page": {"type": "integer", "description": "Items per page (default: 20, max: 50)", "minimum": 1, "maximum": 50}
            }
        }
    },
    {
        "name": "get_my_profile",
        "description": "Get my profile information on FreelanceHunt",
        "schema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_freelancer_portfolio",
        "description": "Get portfolio items for a specific freelancer",
        "schema": {
            "type": "object",
            "properties": {
                "freelancer_id": {"type": "integer", "description": "Freelancer ID", "minimum": 1},
                "page": {"type": "integer", "description": "Page number (default: 1)", "minimum": 1},
                "per_page": {"type": "integer", "description": "Items per page (default: 20, max: 50)", "minimum": 1, "maximum": 50}
            },
            "required": ["freelancer_id"]
        }
    },
    {
        "name": "get_freelancer_reviews",
        "description": "Get reviews for a specific freelancer",
        "schema": {
            "type": "object",
            "properties": {
                "freelancer_id": {"type": "integer", "description": "Freelancer ID", "minimum": 1},
                "page": {"type": "integer", "description": "Page number (default: 1)", "minimum": 1},
                "per_page": {"type": "integer", "description": "Items per page (default: 20, max: 50)", "minimum": 1, "maximum": 50}
            },
            "required": ["freelancer_id"]
        }
    },
    {
        "name": "search_contests",
        "description": "Search for contests on FreelanceHunt",
        "schema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "Page number (default: 1)", "minimum": 1},
                "per_page": {"type": "integer", "description": "Items per page (default: 20, max: 50)", "minimum": 1, "maximum": 50},
                "skill_ids": {"type": "array", "items": {"type": "integer"}, "description": "List of skill IDs to filter by"}
            }
        }
    },
    {
        "name": "get_contest",
        "description": "Get detailed information about a specific contest",
        "schema": {
            "type": "object",
            "properties": {"contest_id": {"type": "integer", "description": "Contest ID", "minimum": 1}},
            "required": ["contest_id"]
        }
    },
    {
        "name": "get_countries",
        "description": "Get list of available countries on FreelanceHunt",
        "schema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_cities",
        "description": "Get list of cities for a specific country on FreelanceHunt",
        "schema": {
            "type": "object",
            "properties": {
                "country_id": {"type": "integer", "description": "Country ID", "minimum": 1}
            },
            "required": ["country_id"]
        }
    }
]

# Мапинг обработчиков
HANDLERS_MAP = {
    "search_projects": handle_search_projects,
    "get_project": handle_get_project,

    "get_freelancer": handle_get_freelancer,
    "get_skills": handle_get_skills,

    "get_threads": handle_get_threads,
    "get_project_bids": handle_get_project_bids,
    "get_project_comments": handle_get_project_comments,
    "get_my_bids": handle_get_my_bids,
    "get_my_profile": handle_get_my_profile,
    "get_freelancer_portfolio": handle_get_freelancer_portfolio,
    "get_freelancer_reviews": handle_get_freelancer_reviews,
    "search_contests": handle_search_contests,
    "get_contest": handle_get_contest,
    "get_countries": handle_get_countries,
    "get_cities": handle_get_cities
}


# ================================================
# MCP Server handlers
# ================================================

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name=tool_config["name"],
            description=tool_config["description"],
            inputSchema=tool_config["schema"]
        )
        for tool_config in TOOLS_CONFIG
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    if not client:
        return [types.TextContent(
            type="text",
            text="Error: FreelanceHunt client not initialized. Please set FREELANCEHUNT_API_KEY environment variable and restart the server."
        )]
    
    try:
        handler = HANDLERS_MAP.get(name)
        if handler:
            return await handler(client, arguments)
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


# ================================================
# Server entry point
# ================================================

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
