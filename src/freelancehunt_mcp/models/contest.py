# ================================================
# Модели для конкурсов
# ================================================

from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

from .base import ProjectSkill, ProjectBudget
from .project import Employer


class ContestAttributes(BaseModel):
    name: str
    description: Optional[str] = None
    description_html: Optional[str] = None
    skill: Optional[ProjectSkill] = None
    status: Optional[Dict[str, Any]] = None
    budget: Optional[ProjectBudget] = None
    application_count: int = 0
    published_at: Optional[datetime] = None
    duration_days: Optional[int] = None
    final_started_at: Optional[datetime] = None
    employer: Optional[Employer] = None
    freelancer: Optional[Dict[str, Any]] = None
    tags: List[Dict[str, Any]] = []
    updates: List[Dict[str, Any]] = []


class Contest(BaseModel):
    id: int
    type: str = "contest"
    attributes: ContestAttributes
    links: Optional[Dict[str, Any]] = None


class ContestsResponse(BaseModel):
    data: List[Contest]
    links: Dict[str, str] = {}
    meta: Optional[Dict[str, Any]] = {}
