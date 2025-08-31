
import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPTestClient:
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
    
    async def connect_to_server(self, server_script_path: str):
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\\nConnected to FreelanceHunt MCP Server!")
        print("Available tools:", [tool.name for tool in tools])
        print()
    
    async def test_tools(self):
        if not self.session:
            print("Error: Not connected to server")
            return
        
        try:
            # Test getting skills list
            print("=== Testing get_skills ===")
            result = await self.session.call_tool("get_skills", {})
            print("Skills result:")
            print(result.content[0].text[:500] + "..." if len(result.content[0].text) > 500 else result.content[0].text)
            print()
            
            # Test getting locations list  
            print("=== Testing get_locations ===")
            result = await self.session.call_tool("get_locations", {})
            print("Locations result:")
            print(result.content[0].text[:500] + "..." if len(result.content[0].text) > 500 else result.content[0].text)
            print()
            
            # Test searching projects
            print("=== Testing search_projects ===")
            result = await self.session.call_tool("search_projects", {
                "page": 1,
                "per_page": 5,
                "only_remote": True
            })
            print("Projects search result:")
            print(result.content[0].text[:1000] + "..." if len(result.content[0].text) > 1000 else result.content[0].text)
            print()
            
            # Test searching freelancers
            print("=== Testing search_freelancers ===")
            result = await self.session.call_tool("search_freelancers", {
                "page": 1,
                "per_page": 3
            })
            print("Freelancers search result:")
            print(result.content[0].text[:1000] + "..." if len(result.content[0].text) > 1000 else result.content[0].text)
            print()
            
        except Exception as e:
            print(f"Error during testing: {e}")
    
    async def interactive_mode(self):
        if not self.session:
            print("Error: Not connected to server")
            return
        
        print("\\n=== Interactive Mode ===")
        print("Available commands:")
        print("1. search_projects [page] [per_page] [only_remote]")
        print("2. get_project <project_id>")
        print("3. search_freelancers [page] [per_page]")
        print("4. get_freelancer <freelancer_id>")
        print("5. get_skills")
        print("6. get_locations")
        print("7. quit")
        print()
        
        while True:
            try:
                command = input("Enter command: ").strip()
                
                if command.lower() == 'quit':
                    break
                
                parts = command.split()
                if not parts:
                    continue
                
                tool_name = parts[0]
                args = {}
                
                if tool_name == "search_projects":
                    if len(parts) > 1:
                        args["page"] = int(parts[1])
                    if len(parts) > 2:
                        args["per_page"] = int(parts[2])
                    if len(parts) > 3:
                        args["only_remote"] = parts[3].lower() == 'true'
                
                elif tool_name == "get_project":
                    if len(parts) < 2:
                        print("Error: project_id is required")
                        continue
                    args["project_id"] = int(parts[1])
                
                elif tool_name == "search_freelancers":
                    if len(parts) > 1:
                        args["page"] = int(parts[1])
                    if len(parts) > 2:
                        args["per_page"] = int(parts[2])
                
                elif tool_name == "get_freelancer":
                    if len(parts) < 2:
                        print("Error: freelancer_id is required")
                        continue
                    args["freelancer_id"] = int(parts[1])
                
                elif tool_name in ["get_skills", "get_locations"]:
                    pass  # No arguments needed
                
                else:
                    print(f"Unknown command: {tool_name}")
                    continue
                
                # Call the tool
                result = await self.session.call_tool(tool_name, args)
                print("\\nResult:")
                print(result.content[0].text)
                print("\\n" + "="*50)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script> [test|interactive]")
        print("  test - Run automated tests")
        print("  interactive - Run interactive mode (default)")
        sys.exit(1)
    
    server_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "interactive"
    
    client = MCPTestClient()
    try:
        await client.connect_to_server(server_path)
        
        if mode == "test":
            await client.test_tools()
        else:
            await client.interactive_mode()
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
