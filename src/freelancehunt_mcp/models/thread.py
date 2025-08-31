# ================================================
# Модели для сообщений и тредов
# ================================================

from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

from .base import Avatar


class ThreadParticipant(BaseModel):
    id: int
    type: str  # "employer" or "freelancer"
    login: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[Avatar] = None


class ThreadParticipants(BaseModel):
    from_: Optional[ThreadParticipant] = Field(None, alias="from")
    to: Optional[ThreadParticipant] = None


class ThreadAttributes(BaseModel):
    subject: Optional[str] = None
    updated_at: Optional[datetime] = None
    messages_count: int = 0
    is_unread: bool = False
    participants: Optional[ThreadParticipants] = None


class Thread(BaseModel):
    id: int
    type: str
    attributes: ThreadAttributes


class ThreadsListResponse(BaseModel):
    data: List[Thread]
    links: Dict[str, str] = {}
    meta: Optional[Dict[str, Any]] = {}
