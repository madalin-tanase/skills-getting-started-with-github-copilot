def test_signup_succeeds_for_existing_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student1@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student2@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_when_activity_is_at_capacity(client):
    # Arrange
    activity_name = "Debate Team"
    seed_email = "seed{index}@mergington.edu"
    overflow_email = "overflow@mergington.edu"

    # Fill participants to the declared max of 10.
    for index in range(2, 11):
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": seed_email.format(index=index)},
        )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": overflow_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
