from flask import Blueprint
from controllers.customerController import get, save, put, delete, get_by_id

customer_blueprint = Blueprint('customer_bp', __name__)
customer_blueprint.route('', methods=['POST'])(save)
customer_blueprint.route('', methods=['GET'])(get)
customer_blueprint.route('/by-id', methods=['PUT'])(put)
customer_blueprint.route('/by-id', methods=['DELETE'])(delete)
customer_blueprint.route('/by-id', methods=['GET'])(get_by_id)
