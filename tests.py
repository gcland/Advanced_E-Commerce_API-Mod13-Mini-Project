import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from faker import Faker
from controllers import customerController 
from database import db  
from datetime import datetime
from models.product import Product
from models.customer import Customer
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
import json

class TestCustomerEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.faker = Faker()
        
    def create_mock_user(self):
        mock_user = MagicMock()
        mock_user.name = self.faker.name()
        mock_user.email = self.faker.email()
        mock_user.phone = self.faker.phone_number()
        return mock_user
    
    @patch('models.schemas.customerSchema.customer_schema.load')
    @patch('services.customerService.save')
    def test_save_customer(self, mock_load, mock_save):
        app = Flask(__name__)
        mock_user = self.create_mock_user()
        test_input = {
            "name": mock_user.name,
            "email": mock_user.email,
            "phone": mock_user.phone
        }
        mock_load.return_value = test_input
        mock_save.return_value = test_input

        with app.test_request_context(json = test_input):
            response, status_code = customerController.save()

        mock_load.assert_called_once_with(test_input)
        mock_save.assert_called_once_with(test_input)

        print('Customer save test:', response, status_code, '\n------------------')
        
        self.assertEqual(status_code, 201)
        self.assertIn("name", response.json)
    
    @patch('services.customerService.get')
    def test_get_customer(self, mock_get):
        mock_user = self.create_mock_user()
        test_input = {
            "name": mock_user.name,
            "email": mock_user.email,
            "phone": mock_user.phone
        }
        
        mock_get.return_value = test_input
    
        with self.app.test_request_context():
            response, status_code = customerController.get()
            
        print('Customer get test:', response, status_code, '\n------------------')
        self.assertEqual(status_code, 200)

class TestProductEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Register the blueprint with the correct URL prefix
        self.app.register_blueprint(product_blueprint, url_prefix='/products')
        
        db.init_app(self.app)
        self.client = self.app.test_client()
        self.faker = Faker()
        
        # Create application context
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    @patch('database.db.session')
    def test_save_product_success(self, mock_session):
        # Prepare test data
        test_data = {
            'name': self.faker.word(),
            'price': float(self.faker.random_number(digits=2)),
            'stock': self.faker.random_int(min=1, max=100),
            'description': self.faker.text(max_nb_chars=200)
        }

        # Create a mock product with an ID
        mock_product = Product(
            id=1,
            name=test_data['name'],
            price=test_data['price'],
            stock=test_data['stock'],
            description=test_data['description']
        )

        # Mock the session behavior
        def mock_add(product):
            # Simulate the database assigning an ID
            product.id = 1
            return None

        mock_session.add.side_effect = mock_add
        mock_session.commit.return_value = None

        # Make the request using the correct URL
        response = self.client.post('/products', json=test_data)
        
        # Assertions
        self.assertEqual(response.status_code, 201)
        response_data = response.get_json()
        self.assertEqual(response_data['name'], test_data['name'])
        self.assertEqual(float(response_data['price']), test_data['price'])
        self.assertEqual(int(response_data['stock']), test_data['stock'])
        self.assertEqual(response_data['description'], test_data['description'])
        print('Product save test:', response, response.status_code, '\n------------------')
        
        # Verify mock calls
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_save_product_missing_required_fields(self):
        # Test missing name
        test_data = {
            'price': float(self.faker.random_number(digits=2)),
            'stock': self.faker.random_int(min=1, max=100)
        }
        response = self.client.post('/products', json=test_data)
        self.assertEqual(response.status_code, 400)
        print('Product missing info test:', response, response.status_code, '\n------------------')
        self.assertIn('Name is required', response.get_json()['error'])

        # Test missing price
        test_data = {
            'name': self.faker.word(),
            'stock': self.faker.random_int(min=1, max=100)
        }
        response = self.client.post('/products', json=test_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Price is required', response.get_json()['error'])

    @patch('database.db.session')
    def test_save_product_database_error(self, mock_session):
        test_data = {
            'name': self.faker.word(),
            'price': float(self.faker.random_number(digits=2)),
            'stock': self.faker.random_int(min=1, max=100),
            'description': self.faker.text(max_nb_chars=200)
        }

        # Mock the database operations to raise an exception
        mock_session.add.return_value = None
        mock_session.commit.side_effect = Exception('Database error')
        
        response = self.client.post('/products', json=test_data)
        
        self.assertEqual(response.status_code, 500)
        print('Product database error test:', response, response.status_code, '\n------------------')
        self.assertIn('error', response.get_json())
        mock_session.rollback.assert_called_once()

    def test_save_product_no_data(self):
        response = self.client.post('/products', json={ })
        self.assertEqual(response.status_code, 400)
        print('Product no info test:', response, response.status_code, '\n------------------')
        self.assertIn('error', response.get_json())

    @patch('database.db.session')
    def test_get_product(self, mock_session):
        response = self.client.get('/products')
        print('Product get test:', response, response.status_code, '\n------------------')
        self.assertEqual(response.status_code, 200)

class OrderTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Register the blueprint with the correct URL prefix
        self.app.register_blueprint(order_blueprint, url_prefix='/orders')
        
        db.init_app(self.app)
        self.client = self.app.test_client()
        self.faker = Faker()
        
        # Create application context
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        
        # Create test customer
        customer = Customer(name="Test Customer", email="test@test.com", phone="123-456-7890")
        db.session.add(customer)
        
        # Create test products
        product1 = Product(name="Test Product 1", price=10.00, stock=100)
        product2 = Product(name="Test Product 2", price=20.00, stock=50)
        db.session.add_all([product1, product2])
        
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # Test empty get request
    def test_get_orders_empty(self):
        response = self.client.get('/orders')
        self.assertEqual(response.status_code, 200)
        print('Order empty get test:', response, response.status_code, '\n------------------')
        self.assertEqual(json.loads(response.data), [])

    # Test order creation
    def test_create_order_success(self):
        order_data = {
            "customer_id": 1,
            "delivery_date": datetime.now().isoformat(),
            "products": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 1}
            ]
        }
        
        response = self.client.post('/orders',
                                  data=json.dumps(order_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['customer_id'], 1)
        self.assertEqual(data['order_total'], 40.00)  # (2 * 10) + (1 * 20)
        print('Order creation test:', response, response.status_code, '\n------------------')

    # Test invalid customer
    def test_create_order_invalid_customer(self):
        order_data = {
            "customer_id": 999,
            "products": [{"product_id": 1, "quantity": 1}]
        }
        
        response = self.client.post('/orders',
                                  data=json.dumps(order_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("Customer not found", json.loads(response.data)['error'])
        print('Order invalid customer test:', response, response.status_code, '\n------------------')

    # Test insufficient stock
    def test_create_order_insufficient_stock(self):
        order_data = {
            "customer_id": 1,
            "products": [{"product_id": 1, "quantity": 1000}]
        }
        
        response = self.client.post('/orders',
                                  data=json.dumps(order_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Insufficient stock", json.loads(response.data)['error'])
        print('Order insufficient stock test:', response, response.status_code, '\n------------------')

    # Test missing data
    def test_create_order_missing_data(self):
        order_data = {"customer_id": 1}  # Missing products
        
        response = self.client.post('/orders',
                                  data=json.dumps(order_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Products are required", json.loads(response.data)['error'])
        print('Order missing data test:', response, response.status_code, '\n------------------')

if __name__ == "__main__":
    unittest.main()
