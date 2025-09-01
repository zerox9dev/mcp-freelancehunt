# ================================================
# Модели для бидов
# ================================================

from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

from .base import ProjectBudget


class BidStatus(BaseModel):
    active: str = "active"
    rejected: str = "rejected"
    winner: str = "winner"


class BidAttributes(BaseModel):
    days: Optional[int] = None
    safe_type: Optional[str] = None
    budget: Optional[ProjectBudget] = None
    comment: Optional[str] = None
    status: Optional[str] = None
    is_hidden: bool = False
    is_winner: bool = False
    freelancer: Optional[Dict[str, Any]] = None
    project: Optional[Dict[str, Any]] = None
    attachment: Optional[str] = None
    published_at: Optional[str] = None  # Изменено на str, так как API возвращает строку


class Bid(BaseModel):
    id: int
    type: str = "bid" 
    attributes: Optional[BidAttributes] = None


class BidsResponse(BaseModel):
    data: List[Bid]
    links: Dict[str, str] = {}
    meta: Optional[Dict[str, Any]] = {}
