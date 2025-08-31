# ================================================
# Модели для проектов
# ================================================

from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

from .base import ProjectSkill, ProjectBudget, Avatar, Tag


class ProjectStatus(BaseModel):
    id: int
    name: str


class Employer(BaseModel):
    id: int
    type: str
    login: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[Avatar] = None
    verification: Optional[Dict[str, Any]] = None
    self: Optional[str] = None


class ProjectAttributes(BaseModel):
    name: str
    description: str
    description_html: Optional[str] = None
    skills: List[ProjectSkill] = []
    status: ProjectStatus
    budget: Optional[ProjectBudget] = None
    employer: Optional[Employer] = None
    freelancer: Optional[Dict[str, Any]] = None
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    bid_count: int = 0
    is_remote_job: bool = True
    is_premium: Optional[bool] = False
    is_personal: Optional[bool] = False
    location: Optional[Dict[str, Any]] = None
    safe_type: Optional[str] = None
    tags: List[Tag] = []
    updates: List[Dict[str, Any]] = []


class ProjectLinks(BaseModel):
    self: Dict[str, str]
    comments: Optional[str] = None
    bids: Optional[str] = None


class Project(BaseModel):
    id: int
    type: str
    attributes: ProjectAttributes
    links: Optional[ProjectLinks] = None


class ProjectsListResponse(BaseModel):
    data: List[Project]
    links: Dict[str, str] = {}
    meta: Optional[Dict[str, Any]] = {}


class ProjectCommentAttributes(BaseModel):
    message: str
    message_html: Optional[str] = None
    likes: int = 0
    level: int = 1
    parent_comment_id: Optional[int] = None
    is_deleted: bool = False
    author: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


class ProjectComment(BaseModel):
    id: int
    type: str = "project_comment"
    attributes: ProjectCommentAttributes


class ProjectCommentsResponse(BaseModel):
    data: List[ProjectComment]
    links: Dict[str, str] = {}
