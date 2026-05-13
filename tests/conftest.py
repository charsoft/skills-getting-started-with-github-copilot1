"""
Pytest configuration and fixtures for API tests.
Provides fixtures for setting up test data and API client.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def test_activities():
    """
    Arrange: Fixture that provides sample test activities.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice and compete in basketball games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": []
        }
    }


@pytest.fixture
def client(test_activities):
    """
    Arrange: Fixture that sets up a test client with isolated test data.
    Replaces the app's in-memory activities with test data for each test.
    """
    # Store original activities
    original_activities = None
    
    # Replace activities with test data
    import src.app
    original_activities = src.app.activities.copy()
    src.app.activities.clear()
    src.app.activities.update(test_activities)
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Cleanup: restore original activities
    src.app.activities.clear()
    src.app.activities.update(original_activities)
