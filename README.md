# FreelanceHunt MCP Server

MCP сервер для интеграции с FreelanceHunt API.

## Установка

```bash
git clone <repository-url>
cd mcp-freelancehunt
uv sync
cp env.example .env
```

Настройте `.env`:
```env
FREELANCEHUNT_API_KEY=your_api_key_here
```

## Использование

```bash
python server.py
```

### Claude Desktop

Добавьте в `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "freelancehunt": {
      "command": "python",
      "args": ["/path/to/mcp-freelancehunt/server.py"]
    }
  }
}
```

## Инструменты

- `search_projects` - поиск проектов
- `get_project` - детали проекта 
- `search_freelancers` - поиск фрилансеров
- `get_freelancer` - профиль фрилансера
- `get_skills` - список навыков
- `get_locations` - список локаций

## Лицензия

MIT