from flask import Blueprint, request, jsonify
from models.mechanic_model import update_mechanic_location, get_mechanic_location

location_routes = Blueprint('location_routes', __name__)

@location_routes.route('/api/mechanic/update-location', methods=['POST'])
def mechanic_update_location():
    data = request.json
    mechanic_id = data.get('mechanic_id')
    lat = data.get('lat')
    lng = data.get('lng')

    update_mechanic_location(mechanic_id, lat, lng)
    return jsonify({'message': 'Location updated'}), 200

@location_routes.route('/api/driver/mechanic-location/<int:mechanic_id>', methods=['GET'])
def driver_get_mechanic_location(mechanic_id):
    location = get_mechanic_location(mechanic_id)
    if not location:
        return jsonify({'message': 'Mechanic not found'}), 404

    return jsonify({
        'lat': location['current_lat'],
        'lng': location['current_lng']
    }), 200
