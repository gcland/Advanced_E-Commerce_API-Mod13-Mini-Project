from flask import Flask
from database import db
from schema import ma
from limiter import limiter
from caching import cache
from sqlalchemy.orm import Session
from password import password
import pymysql
pymysql.install_as_MySQLdb()

from models.customer import Customer
from models.customerAccount import CustomerAccount
from models.order import Order
from models.product import Product
from models.orderProduct import order_product
from models.role import Role
from models.customerManagementRole import CustomerManagementRole

from routes.customerBP import customer_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.customerAccountBP import customerAccount_blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'E-Commerce Application'
    }
)

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{password}@localhost/e_commerce_db'   # For testing with MySQL database; ensure password file is updated with user password.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://advanced_e_commerce_api_postgresql_y5s1_user:8HeVhnCgsCHgnkqqo8d4CTQMcQjRYL9X@dpg-ctrav03qf0us7385dhpg-a.oregon-postgres.render.com/advanced_e_commerce_api_postgresql_y5s1'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)
    # cache.init_app(app)
    # limiter.init_app(app)

    return app

def blue_print_config(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(customerAccount_blueprint, url_prefix='/customerAccounts')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def configure_rate_limit():
    limiter.limit("100 per day")(customer_blueprint)
    limiter.limit("100 per day")(product_blueprint)
    limiter.limit("100 per day")(order_blueprint)
    limiter.limit("100 per day")(product_blueprint)
    limiter.limit("100 per day")(customerAccount_blueprint)

def init_roles_customers_info_data():       # add sample customers and users (customerAccounts) 
    with Session(db.engine) as session:
        with session.begin():
            customers = [
                Customer(name = "Customer_A", email = 'customerA@gmail.com', phone = "123-123-1234"),
                Customer(name = "Customer_G", email = 'customerG@yahoo.com', phone = "456-456-3429"),
                Customer(name = "Customer_Z", email = 'customerZ@outlook.com', phone = "986-567-3452")
            ]

            customerAccounts = [
                CustomerAccount(username = "csA", password = 'passwordA', customer_id=1),
                CustomerAccount(username = "string", password = 'string', customer_id=2),
                CustomerAccount(username = "csC", password = 'passwordC', customer_id=3)  
            ]
            session.add_all(customers)
            session.add_all(customerAccounts)

def init_roles_data():
    with Session(db.engine) as session:
        with session.begin():
            roles = [
                Role(role_name='admin'),
                Role(role_name='customer'),
            ]
            session.add_all(roles)

def init_roles_customers_data():
    with Session(db.engine) as session:
        with session.begin():
            roles_customer = [
                CustomerManagementRole(customer_management_id = 1, role_id=1),
                CustomerManagementRole(customer_management_id = 1, role_id=2),
                CustomerManagementRole(customer_management_id = 2, role_id=2),
                CustomerManagementRole(customer_management_id = 3, role_id=2)
            ]
            session.add_all(roles_customer)


if __name__ == '__main__':
    app = create_app()
    blue_print_config(app)
    # configure_rate_limit()
    app.run(debug=True)

with app.app_context():
    # db.drop_all()
    db.create_all()
    init_roles_customers_info_data()
    # init_roles_data()
    # init_roles_customers_data()
