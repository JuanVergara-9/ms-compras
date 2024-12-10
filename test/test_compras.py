import unittest
from app import create_app, db
from app.models import Compras

class CompraTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_compra_success(self):
        # Datos de prueba
        product_id = 1
        purchase_direction = '123 Calle Falsa'

        compra_data = {
            'product_id': product_id,
            'purchase_direction': purchase_direction
        }
        # Se realiza la solicitud
        response = self.client.post('/compra/add', json=compra_data)
        print(response.data)
        self.assertEqual(response.status_code, 201)

        # Se imprime la respuesta
        response_json = response.get_json()
        print(response_json)

        # Se obtiene el ID de la compra
        compra_id = response_json.get('id_compra')

        # Se verifica que se haya creado correctamente
        try:
            with self.app.app_context():
                compra = Compras.query.filter_by(id_purchase=compra_id).first()
                self.assertIsNotNone(compra)
                self.assertEqual(compra.purchase_direction, compra_data["purchase_direction"])
        
        # Se elimina la compra
        finally:
            with self.app.app_context():
                if compra_id:
                    compra = Compras.query.filter_by(id_purchase=compra_id).first()
                    if compra:
                        db.session.delete(compra)
                        db.session.commit()

    def test_missing_fields(self):
        compra_data = {
            'product_id': 1
        }
        response = self.client.post('/compra/add', json=compra_data)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Missing fields')

if __name__ == '__main__':
    unittest.main()