# src/services/participant_service.py

from src.database.db_manager import DatabaseManager
from src.models.participant import Participant
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class ParticipantService:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def add_participant(self, name, email, event_id):
        """Adiciona um novo participante ao banco de dados"""
        session = self.db_manager.get_session()
        try:
            participant = Participant(
                name=name,
                email=email,
                event_id=event_id,
                registration_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            session.add(participant)
            session.commit()
            return participant
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao adicionar participante: {e}")
        finally:
            session.close()

    def get_participants_by_event(self, event_id):
        """Retorna todos os participantes de um evento"""
        session = self.db_manager.get_session()
        try:
            participants = session.query(Participant).filter_by(event_id=event_id).all()
            return participants
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar participantes: {e}")
        finally:
            session.close()

    def delete_participant(self, participant_id):
        """Remove um participante pelo ID"""
        session = self.db_manager.get_session()
        try:
            participant = session.query(Participant).filter_by(id=participant_id).first()
            if participant:
                session.delete(participant)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao remover participante: {e}")
        finally:
            session.close()