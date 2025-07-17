from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
import logging

Base = declarative_base()
from src.models.event import Event
from src.models.purchase import Purchase

logging.basicConfig(level=logging.DEBUG)

class DatabaseManager:
    def __init__(self, db_path="sqlite:///eventos_igreja.db"):
        self.engine = create_engine(db_path, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Cria as tabelas definidas nos modelos"""
        try:
            logging.debug("Iniciando criação das tabelas")
            Base.metadata.create_all(self.engine)
            logging.debug("Tabelas criadas com sucesso")
        except SQLAlchemyError as e:
            logging.error(f"Erro ao criar tabelas: {e}")
            raise Exception(f"Erro ao criar tabelas: {e}")

    def get_session(self):
        """Retorna uma nova sessão do banco de dados"""
        return self.Session()