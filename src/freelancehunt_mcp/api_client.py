

import asyncio
import os
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode

import httpx
from pydantic import ValidationError

from .models import (
    Project, 
    ProjectsListResponse, 
    FreelancerProfile,
    SearchFilters,
    Thread,
    ThreadsListResponse,
    ProjectCommentsResponse,
    BidsResponse,
    Contest,
    ContestsResponse,
    CountriesResponse,
    PortfolioResponse,
    UserProfile
)


class FreelanceHuntAPIError(Exception):
    pass


class FreelanceHuntClient:
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv('FREELANCEHUNT_API_KEY')
        self.base_url = base_url or os.getenv('FREELANCEHUNT_BASE_URL', 'https://api.freelancehunt.com/v2')
        self.request_delay = float(os.getenv('REQUEST_DELAY', '1.0'))
        
        if not self.api_key:
            raise ValueError("API key is required. Set FREELANCEHUNT_API_KEY environment variable.")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'MCP-FreelanceHunt/0.1.0'
        }
        
        self._last_request_time = 0.0
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Simple rate limiting
        current_time = asyncio.get_event_loop().time()
        if current_time - self._last_request_time < self.request_delay:
            await asyncio.sleep(self.request_delay - (current_time - self._last_request_time))
        
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=data,
                    timeout=30.0
                )
                
                self._last_request_time = asyncio.get_event_loop().time()
                
                if response.status_code == 401:
                    raise FreelanceHuntAPIError("Unauthorized. Check your API key.")
                elif response.status_code == 403:
                    raise FreelanceHuntAPIError("Forbidden. Check your API permissions.")
                elif response.status_code == 404:
                    raise FreelanceHuntAPIError("Resource not found.")
                elif response.status_code == 429:
                    raise FreelanceHuntAPIError("Rate limit exceeded. Please wait.")
                elif response.status_code >= 400:
                    raise FreelanceHuntAPIError(f"API error: {response.status_code} - {response.text}")
                
                return response.json()
                
        except httpx.RequestError as e:
            raise FreelanceHuntAPIError(f"Request failed: {e}")
    
    async def search_projects(
        self,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[SearchFilters] = None
    ) -> ProjectsListResponse:
        params = {
            'page[number]': page,
            'page[size]': min(per_page, 50)  # API limit
        }
        
        # Add filters if provided
        if filters:
            filter_dict = filters.model_dump(exclude_none=True)
            # Convert filters to API 2.0 format
            for key, value in filter_dict.items():
                if key == 'skill_id' and value:
                    params[f'filter[{key}]'] = ','.join(map(str, value))
                elif value is not None:
                    params[f'filter[{key}]'] = value
        
        try:
            response_data = await self._make_request('GET', '/projects', params=params)
            return ProjectsListResponse(**response_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid response format: {e}")
    
    async def get_project(self, project_id: int) -> Project:
        try:
            response_data = await self._make_request('GET', f'/projects/{project_id}')
                        # API 2.0 returns single project in 'data' field
            project_data = response_data.get('data')
            if not project_data:
                raise FreelanceHuntAPIError("No project data in response")
            return Project(**project_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid project data: {e}")
    

    async def get_freelancer(self, freelancer_id: int) -> FreelancerProfile:
        try:
            response_data = await self._make_request('GET', f'/freelancers/{freelancer_id}')
            # API returns single freelancer in 'data' field
            freelancer_data = response_data.get('data', response_data)
            return FreelancerProfile(**freelancer_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid freelancer data: {e}")
    
    async def get_skills(self) -> List[Dict[str, Any]]:
        try:
            response_data = await self._make_request('GET', '/skills')
            return response_data.get('data', [])
        except Exception as e:
            raise FreelanceHuntAPIError(f"Failed to get skills: {e}")
    
    async def get_locations(self) -> List[Dict[str, Any]]:
        """Получить страны (локации верхнего уровня)"""
        try:
            response_data = await self._make_request('GET', '/countries')
            return response_data.get('data', [])
        except Exception as e:
            raise FreelanceHuntAPIError(f"Failed to get locations: {e}")
    
    async def get_cities(self, country_id: int) -> List[Dict[str, Any]]:
        """Получить города для конкретной страны"""
        try:
            response_data = await self._make_request('GET', f'/cities/{country_id}')
            return response_data.get('data', [])
        except Exception as e:
            raise FreelanceHuntAPIError(f"Failed to get cities for country {country_id}: {e}")
    
    async def get_threads(
        self,
        page: int = 1,
        per_page: int = 20
    ) -> ThreadsListResponse:
        params = {
            'page[number]': page,
            'page[size]': min(per_page, 50)  # API limit
        }
        
        try:
            response_data = await self._make_request('GET', '/threads', params=params)
            return ThreadsListResponse(**response_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid threads response format: {e}")
        except Exception as e:
            raise FreelanceHuntAPIError(f"Failed to get threads: {e}")

    # ================================================
    # Дополнительные методы API
    # ================================================
    
    async def get_project_bids(
        self, 
        project_id: int,
        page: int = 1,
        per_page: int = 20
    ) -> BidsResponse:
        """Получить биды проекта"""
        params = {
            'page[number]': page,
            'page[size]': min(per_page, 50)
        }
        
        try:
            response_data = await self._make_request('GET', f'/projects/{project_id}/bids', params=params)
            return BidsResponse(**response_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid bids data: {e}")

    async def get_project_comments(
        self, 
        project_id: int,
        page: int = 1,
        per_page: int = 20
    ) -> ProjectCommentsResponse:
        """Получить комментарии проекта"""
        params = {
            'page[number]': page,
            'page[size]': min(per_page, 50)
        }
        
        try:
            response_data = await self._make_request('GET', f'/projects/{project_id}/comments', params=params)
            return ProjectCommentsResponse(**response_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid comments data: {e}")

    async def get_my_bids(
        self,
        page: int = 1,
        per_page: int = 20
    ) -> BidsResponse:
        """Получить мои биды"""
        params = {
            'page[number]': page,
            'page[size]': min(per_page, 50)
        }
        
        try:
            response_data = await self._make_request('GET', '/my/bids', params=params)
            return BidsResponse(**response_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid my bids data: {e}")

    async def get_my_profile(self) -> UserProfile:
        """Получить мой профиль"""
        try:
            response_data = await self._make_request('GET', '/my/profile')
            profile_data = response_data.get('data')
            if not profile_data:
                raise FreelanceHuntAPIError("No profile data in response")
            return UserProfile(**profile_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid profile data: {e}")

    async def get_freelancer_portfolio(
        self,
        freelancer_id: int,
        page: int = 1,
        per_page: int = 20
    ) -> PortfolioResponse:
        """Получить портфолио фрилансера"""
        params = {
            'page[number]': page,
            'page[size]': min(per_page, 50)
        }
        
        try:
            response_data = await self._make_request('GET', f'/freelancers/{freelancer_id}/portfolio', params=params)
            return PortfolioResponse(**response_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid portfolio data: {e}")

    async def get_freelancer_reviews(
        self,
        freelancer_id: int,
        page: int = 1,
        per_page: int = 20
    ) -> List[Dict[str, Any]]:
        """Получить отзывы о фрилансере"""
        params = {
            'page[number]': page,
            'page[size]': min(per_page, 50)
        }
        
        try:
            response_data = await self._make_request('GET', f'/freelancers/{freelancer_id}/reviews', params=params)
            return response_data.get('data', [])
        except Exception as e:
            raise FreelanceHuntAPIError(f"Failed to get freelancer reviews: {e}")

    async def search_contests(
        self,
        page: int = 1,
        per_page: int = 20,
        skill_ids: Optional[List[int]] = None
    ) -> ContestsResponse:
        """Поиск конкурсов"""
        params = {
            'page[number]': page,
            'page[size]': min(per_page, 50)
        }
        
        if skill_ids:
            params['filter[skill_id]'] = ','.join(map(str, skill_ids))
        
        try:
            response_data = await self._make_request('GET', '/contests', params=params)
            return ContestsResponse(**response_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid contests data: {e}")

    async def get_contest(self, contest_id: int) -> Contest:
        """Получить детали конкурса"""
        try:
            response_data = await self._make_request('GET', f'/contests/{contest_id}')
            contest_data = response_data.get('data')
            if not contest_data:
                raise FreelanceHuntAPIError("No contest data in response")
            return Contest(**contest_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid contest data: {e}")

    async def get_countries(self) -> CountriesResponse:
        """Получить список стран"""
        try:
            response_data = await self._make_request('GET', '/countries')
            return CountriesResponse(**response_data)
        except ValidationError as e:
            raise FreelanceHuntAPIError(f"Invalid countries data: {e}")
