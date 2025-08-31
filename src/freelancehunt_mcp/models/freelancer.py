# ================================================
# Модели для фрилансеров
# ================================================

from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

from .base import ProjectSkill, ProjectBudget, Avatar


class FreelancerAttributes(BaseModel):
    login: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[Avatar] = None
    birth_date: Optional[str] = None
    rating: Optional[int] = None
    rating_position: Optional[int] = None
    arbitrages: int = 0
    positive_reviews: int = 0
    negative_reviews: int = 0
    answered_average_minutes: Optional[int] = None
    is_plus_active: bool = False
    is_online: bool = False
    location: Optional[Dict[str, Any]] = None
    verification: Optional[Dict[str, Any]] = None
    contacts: Optional[Dict[str, Any]] = None
    plus_ends_at: Optional[str] = None
    active_projects: int = 0
    completed_projects: int = 0
    completed_contests: int = 0
    success_rate: Optional[float] = None
    average_grade: Optional[float] = None
    view_count: Optional[int] = None
    created_at: Optional[str] = None
    visited_at: Optional[str] = None
    status: Optional[Dict[str, Any]] = None
    cv: Optional[str] = None
    cv_html: Optional[str] = None
    skills: List[ProjectSkill] = []
    snippet_count: int = 0


class FreelancerProfile(BaseModel):
    id: int
    type: str
    attributes: FreelancerAttributes
    links: Optional[Dict[str, Any]] = None


class UserProfile(BaseModel):
    id: int
    type: str  # "freelancer" or "employer"
    attributes: FreelancerAttributes
    links: Optional[Dict[str, Any]] = None


class PortfolioItem(BaseModel):
    id: int
    type: str = "snippet"
    name: Optional[str] = None
    file_type: Optional[str] = None
    skill: Optional[ProjectSkill] = None
    comment: Optional[str] = None
    url: Optional[str] = None
    amount: Optional[float] = None
    image: Optional[Dict[str, Any]] = None
    views: int = 0
    votes: int = 0
    created_at: Optional[datetime] = None


class PortfolioResponse(BaseModel):
    data: List[PortfolioItem]
    links: Dict[str, str] = {}
