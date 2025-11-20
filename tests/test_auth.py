import pytest

from app import create_app, db, User


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, name="Test User", email="user@example.com", password="password123"):
    return client.post(
        "/register",
        data={"name": name, "email": email, "password": password},
        follow_redirects=True,
    )


def login(client, email="user@example.com", password="password123"):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


def test_register_creates_user_and_redirects(client):
    response = register(client)
    assert response.status_code == 200
    assert b"Account created successfully" in response.data
    assert b"Dashboard" in response.data


def test_login_with_valid_credentials(client):
    register(client)
    response = login(client)
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data
    assert b"Dashboard" in response.data


def test_dashboard_requires_authentication(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Please log in" in response.data or b"Invalid email or password" in response.data


def test_login_rejects_invalid_password(client):
    register(client)
    response = login(client, password="wrongpass")
    assert b"Invalid email or password" in response.data
    assert b"Dashboard" not in response.data


def test_prevents_duplicate_email_registration(client):
    register(client)
    response = register(client)
    assert b"already exists" in response.data
    assert response.status_code == 200
