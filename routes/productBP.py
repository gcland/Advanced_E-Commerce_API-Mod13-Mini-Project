from flask import Blueprint
from controllers.productController import get, save, find_all_pagination, put, delete, get_by_id

product_blueprint = Blueprint('product_bp', __name__)
product_blueprint.route('/', methods=['POST'])(save)
product_blueprint.route('/', methods=['GET'])(get)
product_blueprint.route('/paginate', methods=['GET'])(find_all_pagination)
product_blueprint.route('/by-id', methods=['PUT'])(put)
product_blueprint.route('/by-id', methods=['DELETE'])(delete)
product_blueprint.route('/by-id', methods=['GET'])(get_by_id)