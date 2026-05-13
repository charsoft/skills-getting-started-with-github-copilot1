"""
Integration tests for API endpoints using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Client with test data is ready
        Act: Make GET request to /activities
        Assert: Verify all activities are returned with correct structure
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 3
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Basketball Team" in activities

    def test_get_activities_includes_participants(self, client):
        """
        Arrange: Client with test data
        Act: Get activities
        Assert: Verify participants are included in response
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert activities["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]
        assert activities["Programming Class"]["participants"] == ["emma@mergington.edu"]
        assert activities["Basketball Team"]["participants"] == []


class TestPostSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client):
        """
        Arrange: Client and test data with empty Basketball Team
        Act: Sign up new student for Basketball Team
        Assert: Verify signup is successful and participant is added
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "john@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity_name]["participants"]

    def test_signup_duplicate_fails(self, client):
        """
        Arrange: Client with Chess Club already having michael@mergington.edu
        Act: Try signing up same student for same activity
        Assert: Verify 400 error is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_not_found(self, client):
        """
        Arrange: Client with test data
        Act: Try signing up for non-existent activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestDeleteUnregister:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_unregister_successful(self, client):
        """
        Arrange: Client with Chess Club having michael@mergington.edu
        Act: Unregister michael from Chess Club
        Assert: Verify unregister is successful and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()[activity_name]["participants"]

    def test_unregister_participant_not_found(self, client):
        """
        Arrange: Client with Basketball Team having no participants
        Act: Try unregistering non-existent participant
        Assert: Verify 400 error is returned
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "nonexistent@example.com"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_activity_not_found(self, client):
        """
        Arrange: Client with test data
        Act: Try unregistering from non-existent activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@example.com"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestGetRoot:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_index(self, client):
        """
        Arrange: Client is ready
        Act: Make GET request to /
        Assert: Verify redirect to static/index.html
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
