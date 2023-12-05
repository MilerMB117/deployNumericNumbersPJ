import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Configuración para las pruebas
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Métodos Numéricos'.encode('utf-8'), response.data)

    def test_results(self):
        response = self.app.get('/results')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Resultados'.encode('utf-8'), response.data)

    def test_about(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Acerca de'.encode('utf-8'), response.data)

    # Agrega más pruebas según sea necesario

    def test_calculate(self):
        data = {'equation': 'x**2 - 4', 'method': 'Punto Fijo'}
        response = self.app.post('/calculate', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Gráfico de la Función'.encode('utf-8'), response.data)
        # Agrega más afirmaciones según sea necesario

if __name__ == '__main__':
    unittest.main()
