# FreelanceHunt MCP Server

MCP сервер для FreelanceHunt API v2. **16 tools, 100% работают.*

## Установка

```bash
uv sync
cp env.example .env
# Добавь FREELANCEHUNT_API_KEY в .env
python src/freelancehunt_mcp/server.py
```

## Tools

**Проекты:** `search_projects`, `get_project`, `get_project_bids`, `get_project_comments`

**Фрилансеры:** `get_freelancer`, `get_freelancer_portfolio`, `get_freelancer_reviews`

**Личное:** `get_my_profile`, `get_my_bids`

**Конкурсы:** `search_contests`, `get_contest`

**Коммуникации:** `get_threads`

**География:** `get_countries`, `get_cities`

**Справочники:** `get_skills`

## Claude Desktop

```json
{
  "mcpServers": {
    "freelancehunt": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {"FREELANCEHUNT_API_KEY": "your_key"}
    }
  }
}
```