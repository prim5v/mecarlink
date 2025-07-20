from flask import Blueprint, request, jsonify
from models.company_model import create_company, get_company_by_email
from utils.auth import hash_password, verify_password

company_routes = Blueprint('company_routes', __name__)

@company_routes.route('/api/company/register', methods=['POST'])
def register_company():
    data = request.json
    existing = get_company_by_email(data['email'])
    if existing:
        return jsonify({'message': 'Company already exists'}), 409

    data['password'] = hash_password(data['password'])
    create_company(data)
    return jsonify({'message': 'Company registered successfully'}), 201

@company_routes.route('/api/company/login', methods=['POST'])
def login_company():
    data = request.json
    company = get_company_by_email(data['email'])
    if not company or not verify_password(data['password'], company['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'company_id': company['id']}), 200
