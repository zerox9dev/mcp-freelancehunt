# ================================================
# Модели для локаций и географии
# ================================================

from typing import List, Optional, Any, Dict
from pydantic import BaseModel


# Используем уже определенную в base.py модель Country
# Здесь можем добавить дополнительные географические модели при необходимости

class Location(BaseModel):
    id: int
    name: str
    country_id: Optional[int] = None
    country: Optional[Dict[str, Any]] = None
