from src.database.db_manager import DatabaseManager
from src.models.purchase import Purchase
from src.models.event import Event
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class PurchaseService:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def add_purchase(self, buyer_name, event_id, ticket_quantity, unit_price, payment_method):
        """Adiciona uma nova compra ao banco de dados"""
        session = self.db_manager.get_session()
        try:
            purchase = Purchase(
                buyer_name=buyer_name,
                purchase_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                event_id=event_id,
                ticket_quantity=ticket_quantity,
                unit_price=unit_price,
                payment_method=payment_method
            )
            session.add(purchase)
            session.commit()
            return purchase
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao adicionar compra: {e}")
        finally:
            session.close()

    def get_purchases_by_event(self, event_id):
        """Retorna todas as compras de um evento"""
        session = self.db_manager.get_session()
        try:
            purchases = session.query(Purchase).filter_by(event_id=event_id).all()
            return purchases
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar compras: {e}")
        finally:
            session.close()

    def delete_purchase(self, purchase_id):
        """Remove uma compra pelo ID"""
        session = self.db_manager.get_session()
        try:
            purchase = session.query(Purchase).filter_by(id=purchase_id).first()
            if purchase:
                session.delete(purchase)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao remover compra: {e}")
        finally:
            session.close()

    def get_all_events(self):
        """Retorna todos os eventos disponíveis"""
        session = self.db_manager.get_session()
        try:
            events = session.query(Event).all()
            return events
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar eventos: {e}")
        finally:
            session.close()

    def add_event(self, name, date, location):
        """Adiciona um novo evento ao banco de dados"""
        session = self.db_manager.get_session()
        try:
            existing_event = session.query(Event).filter_by(name=name, date=date).first()
            if existing_event:
                raise Exception("Já existe um evento com o mesmo nome e data!")
            
            event = Event(name=name, date=date, location=location)
            session.add(event)
            session.commit()
            return event.id
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao adicionar evento: {e}")
        finally:
            session.close()

    def get_all_buyer_names(self):
        """Retorna todos os nomes distintos de compradores"""
        session = self.db_manager.get_session()
        try:
            names = session.query(Purchase.buyer_name).distinct().all()
            return [name.buyer_name for name in names]
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao buscar nomes de compradores: {e}")
        finally:
            session.close()

    def check_existing_purchase(self, buyer_name, event_id, unit_price, payment_method):
        """Verifica se o comprador já tem uma compra para o evento com o mesmo preço e método de pagamento"""
        session = self.db_manager.get_session()
        try:
            existing_purchase = session.query(Purchase).filter_by(
                buyer_name=buyer_name,
                event_id=event_id,
                unit_price=unit_price,
                payment_method=payment_method
            ).first()
            return existing_purchase  # Return the Purchase object or None
        except SQLAlchemyError as e:
            raise Exception(f"Erro ao verificar compra existente: {e}")
        finally:
            session.close()

    def update_purchase_quantity(self, purchase_id, new_quantity):
        """Atualiza a quantidade de ingressos de uma compra existente"""
        session = self.db_manager.get_session()
        try:
            purchase = session.query(Purchase).filter_by(id=purchase_id).first()
            if purchase:
                purchase.ticket_quantity = new_quantity
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Erro ao atualizar quantidade da compra: {e}")
        finally:
            session.close()