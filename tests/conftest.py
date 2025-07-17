# conftest.py

import pytest
from src.database.db_manager import DatabaseManager
from src.models.participant import Base

@pytest.fixture(scope="session")
def db_manager():
    """Fixture para criar e gerenciar o banco de dados de teste"""
    db = DatabaseManager("sqlite:///test_eventos_igreja.db")
    Base.metadata.create_all(db.engine)
    yield db
    Base.metadata.drop_all(db.engine)

@pytest.fixture
def db_session(db_manager):
    """Fixture para criar uma sessão de banco de dados"""
    session = db_manager.get_session()
    yield session
    session.close()