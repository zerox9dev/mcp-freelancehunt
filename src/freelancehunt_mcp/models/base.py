# ================================================
# Базовые модели и общие типы
# ================================================

from datetime import datetime
from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel, Field


class Avatar(BaseModel):
    small: Dict[str, Any]
    large: Dict[str, Any]


class ProjectSkill(BaseModel):
    id: int
    name: str


class ProjectBudget(BaseModel):
    amount: Optional[float] = None
    currency: str = "UAH"
    per_hour: Optional[bool] = None


class Tag(BaseModel):
    id: int
    name: str


class Country(BaseModel):
    id: int
    iso2: str
    name: str


class CountriesResponse(BaseModel):
    data: List[Country]
    links: Dict[str, str] = {}
