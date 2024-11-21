from flask import Blueprint
from controllers.customerAccountController import get, save, put, delete, login, get_by_id

customerAccount_blueprint = Blueprint('customerAccount_bp', __name__)
customerAccount_blueprint.route('/', methods=['GET'])(get)
customerAccount_blueprint.route('/', methods=['POST'])(save)
customerAccount_blueprint.route('/by-id', methods=['PUT'])(put)
customerAccount_blueprint.route('/by-id', methods=['DELETE'])(delete)
customerAccount_blueprint.route('/login', methods=['POST'])(login)
customerAccount_blueprint.route('/by-id', methods=['GET'])(get_by_id)
