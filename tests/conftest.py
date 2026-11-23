import os
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["ADMIN_API_KEY"] = "test-secret"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.base import Base, get_db
from app.main import app

@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    def override():
        with factory() as session:
            yield session
    app.dependency_overrides[get_db] = override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    engine.dispose()
