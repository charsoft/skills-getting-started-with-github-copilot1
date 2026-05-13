"""
Unit tests for model and business logic using the AAA (Arrange-Assert-Act) pattern.
"""

import pytest


class TestActivityValidation:
    """Tests for activity validation logic"""

    def test_activity_has_required_fields(self, test_activities):
        """
        Arrange: Sample test activity data
        Act: Check if activity has all required fields
        Assert: Verify all required fields are present
        """
        # Arrange
        activity = test_activities["Chess Club"]
        
        # Act & Assert
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for field in required_fields:
            assert field in activity

    def test_participants_list_type(self, test_activities):
        """
        Arrange: Sample test activities
        Act: Check type of participants field
        Assert: Verify participants is a list
        """
        # Arrange
        activity = test_activities["Programming Class"]
        
        # Act & Assert
        assert isinstance(activity["participants"], list)

    def test_max_participants_is_integer(self, test_activities):
        """
        Arrange: Sample test activities
        Act: Check type of max_participants field
        Assert: Verify max_participants is an integer
        """
        # Arrange
        activity = test_activities["Basketball Team"]
        
        # Act & Assert
        assert isinstance(activity["max_participants"], int)
        assert activity["max_participants"] > 0

    def test_all_activities_have_required_fields(self, test_activities):
        """
        Arrange: All test activities
        Act: Check each activity has required fields
        Assert: Verify all activities conform to schema
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act & Assert
        for activity_name, activity in test_activities.items():
            for field in required_fields:
                assert field in activity, f"{activity_name} missing field {field}"


class TestParticipantOperations:
    """Tests for participant list operations"""

    def test_adding_participant_to_empty_list(self, test_activities):
        """
        Arrange: Activity with no participants
        Act: Add a participant to the list
        Assert: Verify participant count increases
        """
        # Arrange
        activity = test_activities["Basketball Team"]
        original_count = len(activity["participants"])
        new_participant = "alice@example.com"
        
        # Act
        activity["participants"].append(new_participant)
        
        # Assert
        assert len(activity["participants"]) == original_count + 1
        assert new_participant in activity["participants"]

    def test_removing_participant(self, test_activities):
        """
        Arrange: Activity with existing participants
        Act: Remove a participant from the list
        Assert: Verify participant is removed and count decreases
        """
        # Arrange
        activity = test_activities["Chess Club"]
        original_count = len(activity["participants"])
        participant_to_remove = "michael@mergington.edu"
        
        # Act
        activity["participants"].remove(participant_to_remove)
        
        # Assert
        assert len(activity["participants"]) == original_count - 1
        assert participant_to_remove not in activity["participants"]

    def test_checking_participant_membership(self, test_activities):
        """
        Arrange: Activity with known participants
        Act: Check if specific participant is in the list
        Assert: Verify membership check works correctly
        """
        # Arrange
        activity = test_activities["Programming Class"]
        existing_participant = "emma@mergington.edu"
        non_existing_participant = "bob@example.com"
        
        # Act & Assert
        assert existing_participant in activity["participants"]
        assert non_existing_participant not in activity["participants"]

    def test_multiple_participants_in_list(self, test_activities):
        """
        Arrange: Activity with multiple participants
        Act: Check count of participants
        Assert: Verify correct number of participants
        """
        # Arrange
        activity = test_activities["Chess Club"]
        
        # Act
        participant_count = len(activity["participants"])
        
        # Assert
        assert participant_count == 2


class TestAvailabilityCalculation:
    """Tests for calculating available spots"""

    def test_available_spots_with_participants(self, test_activities):
        """
        Arrange: Activity with some participants
        Act: Calculate available spots
        Assert: Verify correct calculation
        """
        # Arrange
        activity = test_activities["Chess Club"]
        
        # Act
        available_spots = activity["max_participants"] - len(activity["participants"])
        
        # Assert
        assert available_spots == 10  # 12 max - 2 participants

    def test_available_spots_empty_activity(self, test_activities):
        """
        Arrange: Activity with no participants
        Act: Calculate available spots
        Assert: Verify all spots are available
        """
        # Arrange
        activity = test_activities["Basketball Team"]
        
        # Act
        available_spots = activity["max_participants"] - len(activity["participants"])
        
        # Assert
        assert available_spots == activity["max_participants"]

    def test_available_spots_full_activity(self, test_activities):
        """
        Arrange: Set activity to be full
        Act: Calculate available spots
        Assert: Verify zero spots available
        """
        # Arrange
        activity = test_activities["Programming Class"]
        max_participants = activity["max_participants"]
        # Fill the activity
        for i in range(max_participants - len(activity["participants"])):
            activity["participants"].append(f"student{i}@example.com")
        
        # Act
        available_spots = activity["max_participants"] - len(activity["participants"])
        
        # Assert
        assert available_spots == 0
