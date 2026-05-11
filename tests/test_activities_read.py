def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_count = 9

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) == expected_activity_count
    assert "Chess Club" in payload
    assert "Programming Class" in payload


def test_get_activities_shows_updated_participants_after_signup(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new-student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert activities_response.status_code == 200
    payload = activities_response.json()
    assert email in payload[activity_name]["participants"]
