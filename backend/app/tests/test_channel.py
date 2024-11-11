import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db, Base
from alembic.config import Config
from alembic import command

# Путь к тестовой базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Применяем миграции Alembic
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

# Фикстура для тестовой базы данных
@pytest.fixture(scope="module")
def db():
    apply_migrations()
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Фикстура для клиента тестирования
@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Фикстура для получения токена авторизации
@pytest.fixture(scope="module")
def auth_token(client):
    # Создание пользователя
    register = client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    # Вход для получения токена
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "password123"}
    )
    token = response.json()["access_token"]
    return f"Bearer {token}"

# Тест для успешного создания канала
def test_create_channel(client, auth_token):
    response = client.post(
        "/channels",
        json={
            "name": "general",
            "is_private": False,
            "topic": "General discussion",
            "admin_email": "test@example.com"
        },
        headers={"Authorization": auth_token}
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Channel created successfully"
    assert response.json()["channel"]["name"] == "general"

# Тест для создания канала с повторяющимся именем
def test_create_duplicate_channel(client, auth_token):
    response = client.post(
        "/channels",
        json={
            "name": "general",
            "is_private": False,
            "topic": "General discussion",
            "admin_email": "test@example.com"
        },
        headers={"Authorization": auth_token}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Channel with this name already exists"
