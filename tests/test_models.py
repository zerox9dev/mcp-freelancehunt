

import pytest
from datetime import datetime
from freelancehunt_mcp.models import (
    Project,
    ProjectStatus,
    ProjectSkill,
    ProjectBudget,
    Employer,
    FreelancerProfile,
    SearchFilters
)


def test_project_status():
    status = ProjectStatus(id=1, name="Active")
    assert status.id == 1
    assert status.name == "Active"


def test_project_skill():
    skill = ProjectSkill(id=1, name="Python")
    assert skill.id == 1
    assert skill.name == "Python"


def test_project_budget():
    budget = ProjectBudget(amount=1000.0, currency="USD", per_hour=False)
    assert budget.amount == 1000.0
    assert budget.currency == "USD"
    assert budget.per_hour is False


def test_employer():
    employer = Employer(
        id=1,
        login="testemployer",
        first_name="John",
        last_name="Doe"
    )
    assert employer.id == 1
    assert employer.login == "testemployer"
    assert employer.first_name == "John"
    assert employer.last_name == "Doe"


def test_project():
    project = Project(
        id=1,
        name="Test Project",
        description="Test Description",
        status=ProjectStatus(id=1, name="Active"),
        bid_count=5
    )
    assert project.id == 1
    assert project.name == "Test Project"
    assert project.description == "Test Description"
    assert project.status.name == "Active"
    assert project.bid_count == 5
    assert project.is_remote_job is True  # default value


def test_freelancer_profile():
    freelancer = FreelancerProfile(
        id=1,
        login="testfreelancer",
        first_name="Jane",
        last_name="Smith",
        rating=4.8,
        reviews_count=25
    )
    assert freelancer.id == 1
    assert freelancer.login == "testfreelancer"
    assert freelancer.rating == 4.8
    assert freelancer.reviews_count == 25


def test_search_filters():
    filters = SearchFilters(
        skill_id=[1, 2, 3],
        budget_from=500.0,
        budget_to=2000.0,
        only_remote=True
    )
    assert filters.skill_id == [1, 2, 3]
    assert filters.budget_from == 500.0
    assert filters.budget_to == 2000.0
    assert filters.only_remote is True


def test_search_filters_empty():
    filters = SearchFilters()
    assert filters.skill_id is None
    assert filters.budget_from is None
    assert filters.budget_to is None
    assert filters.only_remote is None
