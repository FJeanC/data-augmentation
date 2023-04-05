from fastapi.testclient import TestClient
from routes import app

client = TestClient(app)

# Post
def test_create_operation():
    # Arrange
    data = {
            "operation_type": "noise|flip|random_rotation|grayscale",
            "status": "Sucess", 
            "ope_start_time": "17:29:00",
        }
    # Act
    response = client.post("/register", json=data)
    # Assert
    assert response.status_code == 200
    assert response.json()["operation_type"] == data["operation_type"]
    assert response.json()["status"] == data["status"]
    assert response.json()["ope_start_time"] == data["ope_start_time"]

# Get
def test_get_operations():
    # Act
    response = client.get("/register")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Get com parâmetro
def test_get_operations_by_status():
    # Act
    response = client.get("/register?status=Success")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(message["status"] == "Success" for message in response.json())

# Put
def test_update_operation():
    # Arrange
    data = {
            "operation_type": "flip",
            "status": "Success",
            "ope_start_time": "17:47:00"
        }
    # Act
    response = client.put("/register/7", json=data)
    # Assert
    assert response.status_code == 200
    assert response.json()["operation_type"] == data["operation_type"]
    assert response.json()["status"] == data["status"]
    assert "ope_end_time" in response.json()

# Delete
def test_delete_operation():
    # Act
    response = client.delete("/register/8")
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Frame register deleted"}
