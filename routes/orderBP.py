from flask import Blueprint
from services.orderService import get, save, find_all_pagination, put, delete, get_by_id, get_all_by_customer_id

order_blueprint = Blueprint('order_bp', __name__)
order_blueprint.route('', methods=['POST'])(save)
order_blueprint.route('', methods=['GET'])(get)
order_blueprint.route('/paginate', methods=['GET'])(find_all_pagination)
order_blueprint.route('/by-id', methods=['PUT'])(put)
order_blueprint.route('/by-id', methods=['DELETE'])(delete)
order_blueprint.route('/by-id', methods=['GET'])(get_by_id)
order_blueprint.route('/all_by-customer_id', methods=['GET'])(get_all_by_customer_id)