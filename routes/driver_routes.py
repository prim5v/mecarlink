from flask import Blueprint, request, jsonify
from models.driver_model import create_driver, get_driver_by_phone
from utils.auth import hash_password, verify_password

driver_routes = Blueprint('driver_routes', __name__)


@driver_routes.route('/api/driver/register', methods=['POST'])
def register_driver():
    data = request.json
    existing = get_driver_by_phone(data['phone'])
    if existing:
        return jsonify({'message': 'Driver already exists'}), 409

    data['password'] = hash_password(data['password'])
    create_driver(data)
    return jsonify({'message': 'Driver registered successfully'}), 201


@driver_routes.route('/api/driver/login', methods=['POST'])
def login_driver():
    data = request.json
    driver = get_driver_by_phone(data['phone'])
    if not driver or not verify_password(data['password'], driver['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'driver_id': driver['id']}), 200
