from datetime import datetime
from app.models import db, Compras
from app.extension import r
import json
from pybreaker import CircuitBreaker, CircuitBreakerError

breaker = CircuitBreaker(fail_max=10, reset_timeout=10)

class CompraService:
    @staticmethod
    @breaker
    def add_compra(data):
        required_fields = ['product_id', 'purchase_direction']
        if data is None or not all(field in data for field in required_fields):
            return {'error': 'Missing fields'}, 400
        
        try:
            new_compra = Compras(
                product_id=data['product_id'],
                purchase_date=datetime.utcnow(),
                purchase_direction=data['purchase_direction']
            )

            compra_data = {
                'id_compra': new_compra.id_purchase,
                'product_id': new_compra.product_id,
                'purchase_direction': new_compra.purchase_direction
            }
            
            r.set(f"compra:{new_compra.id_purchase}", json.dumps(compra_data), ex=3600)

            db.session.add(new_compra)
            db.session.commit()

            return {
                'message': 'Compra added successfully',
                'id_compra': new_compra.id_purchase
            }, 201
        
        except CircuitBreakerError:
            return {'error': 'Circuito Abierto'}, 500
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @staticmethod
    @breaker
    def remove_compra(data):
        if not 'id_compra' in data:
            return {'error': 'Missing fields'}, 400
        
        try:
            compra = Compras.query.get(data['id_compra'])
            
            if not compra:
                return {'error': 'Compra not found'}, 404
            
            db.session.delete(compra)
            db.session.commit()
            return {'message': 'Compra removed successfully'}, 200
        
        except CircuitBreakerError:
            return {'error': 'Circuito Abierto'}, 500
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500