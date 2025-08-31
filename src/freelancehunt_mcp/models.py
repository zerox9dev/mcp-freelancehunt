

from datetime import datetime
from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel, Field


class ProjectStatus(BaseModel):
    id: int
    name: str


class ProjectSkill(BaseModel):
    id: int
    name: str


class ProjectBudget(BaseModel):
    amount: Optional[float] = None
    currency: str = "UAH"
    per_hour: Optional[bool] = None


class Avatar(BaseModel):
    small: Dict[str, Any]
    large: Dict[str, Any]


class Employer(BaseModel):
    id: int
    type: str
    login: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[Avatar] = None
    verification: Optional[Dict[str, Any]] = None
    self: Optional[str] = None


class Tag(BaseModel):
    id: int
    name: str


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


class FreelancerProfile(BaseModel):
    id: int
    login: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: int = 0
    skills: List[ProjectSkill] = []
    hourly_rate: Optional[ProjectBudget] = None
    location: Optional[Dict[str, Any]] = None
    verification: Optional[Dict[str, Any]] = None


class ProjectsListResponse(BaseModel):
    data: List[Project]
    links: Dict[str, str] = {}
    meta: Optional[Dict[str, Any]] = {}


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


class SearchFilters(BaseModel):
    skill_id: Optional[List[int]] = None
    budget_from: Optional[float] = None
    budget_to: Optional[float] = None
    employer_id: Optional[int] = None
    status_id: Optional[int] = None
    only_remote: Optional[bool] = None
    location_id: Optional[int] = None
