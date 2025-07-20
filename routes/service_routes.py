from flask import Blueprint, request, jsonify
from models.service_model import (
    create_service_request, 
    assign_mechanic_to_request, 
    get_available_mechanic,
    update_mechanic_location,      # ✅ Add this
    get_mechanic_location          # ✅ Add this
)

from models.mechanic_model import update_mechanic_availability  # to be created

service_routes = Blueprint('service_routes', __name__)

@service_routes.route('/api/service/request', methods=['POST'])
def request_service():
    data = request.json
    create_service_request(data)

    mechanic = get_available_mechanic(data['company_id'], data['car_type'])
    
    if not mechanic:
        return jsonify({'message': 'No available mechanic found'}), 404

    # Assign mechanic
    request_id = get_last_inserted_request_id()  # implement this or return ID from create
    assign_mechanic_to_request(request_id, mechanic['id'])

    update_mechanic_availability(mechanic['id'], False)

    return jsonify({
        'message': 'Service request assigned',
        'mechanic': mechanic
    }), 200

@service_routes.route('/api/mechanic/update-location', methods=['POST'])
def update_location():
    data = request.json
    request_id = data.get('request_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not all([request_id, latitude, longitude]):
        return jsonify({'error': 'Missing data'}), 400

    update_mechanic_location(request_id, latitude, longitude)
    return jsonify({'message': 'Mechanic location updated'}), 200


@service_routes.route('/api/mechanic/location/<int:request_id>', methods=['GET'])
def get_location(request_id):
    location = get_mechanic_location(request_id)
    if location:
        return jsonify({
            'latitude': location[0],
            'longitude': location[1]
        }), 200
    else:
        return jsonify({'error': 'Location not found'}), 404
