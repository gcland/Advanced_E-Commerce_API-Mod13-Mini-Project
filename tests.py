import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from faker import Faker
from controllers import customerController 
from controllers import orderController 
from controllers import productController 
from datetime import date

class TestCustomerEndpoints(unittest.TestCase):
    @patch('models.schemas.customerSchema.customer_schema.load')
    @patch('services.customerService.save')
    def test_save_customer(self, mock_load, mock_save):
        app = Flask(__name__)
        app.config['TESTING'] = True
        faker = Faker()
        mock_user = MagicMock()
        mock_user.name = faker.name()
        mock_user.email = faker.email()
        mock_user.phone = faker.phone_number()
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

        print(response, status_code)
        
        self.assertEqual(status_code, 201)
        self.assertIn("name", response.json)
    
    @patch('services.customerService.get')
    def test_get_customer(self, mock_get):
        app = Flask(__name__)
        app.config['TESTING'] = True
        faker = Faker()
        mock_user = MagicMock()
        mock_user.name = faker.name()
        mock_user.email = faker.email()
        mock_user.phone = faker.phone_number()
        test_input = {
            "name": mock_user.name,
            "email": mock_user.email,
            "phone": mock_user.phone

        }
        mock_get.return_value = test_input

        with app.test_request_context():
            response, status_code = customerController.get()

        print(response, status_code)
        
        self.assertEqual(status_code, 200)


class TestProductEndpoints(unittest.TestCase):
    @patch('models.schemas.productSchema.product_schema.load')
    @patch('services.productService.save')
    def test_save_product(self, mock_load, mock_save):
        app = Flask(__name__)
        app.config['TESTING'] = True
        faker = Faker()
        mock_product = MagicMock()
        mock_product.name = faker.name()
        mock_product.price = faker.random_number()
        test_input = {
            "name": mock_product.name,
            "price": mock_product.price

        }
        mock_load.return_value = test_input
        mock_save.return_value = test_input

        with app.test_request_context(json = test_input):
            response, status_code = productController.save()

        mock_load.assert_called_once_with(test_input)
        mock_save.assert_called_once_with(test_input)

        print(response, status_code)
        
        self.assertEqual(status_code, 201)
        self.assertIn("name", response.json)
    
    @patch('services.productService.get')
    def test_get_product(self, mock_get):
        app = Flask(__name__)
        app.config['TESTING'] = True
        faker = Faker()
        mock_product = MagicMock()
        mock_product.name = faker.name()
        mock_product.price = faker.random_number()
        test_input = {
            "name": mock_product.name,
            "price": mock_product.price

        }
        mock_get.return_value = test_input

        with app.test_request_context():
            response, status_code = productController.get()

        print(response, status_code)
        
        self.assertEqual(status_code, 200)

class TestOrderEndpoints(unittest.TestCase):    
    @patch('services.orderService.get')
    def test_get_order(self, mock_get):
        app = Flask(__name__)
        app.config['TESTING'] = True
        faker = Faker()
        mock_order = MagicMock()
        mock_order.customer_id = faker.random_number()
        mock_order.date = faker.date()
        mock_order.products = [{"id": 1}, {"id": 2}, {"id": 5}]
        test_input = {
            "customer_id": mock_order.customer_id,
            "date": mock_order.date,
            "products": mock_order.products
        }

        mock_get.return_value = test_input

        with app.test_request_context():
            response, status_code = orderController.get()

        print(response, status_code)
        
        self.assertEqual(status_code, 200)

if __name__ == "__main__":
    unittest.main()
