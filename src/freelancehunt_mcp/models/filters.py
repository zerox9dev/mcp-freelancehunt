# ================================================
# Модели для фильтров поиска
# ================================================

from typing import List, Optional
from pydantic import BaseModel


class SearchFilters(BaseModel):
    skill_id: Optional[List[int]] = None
    budget_from: Optional[float] = None
    budget_to: Optional[float] = None
    employer_id: Optional[int] = None
    status_id: Optional[int] = None
    only_remote: Optional[bool] = None
    location_id: Optional[int] = None
