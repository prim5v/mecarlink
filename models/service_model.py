from db_config import get_db_connection
import math

def create_service_request(data, mechanic):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """
    INSERT INTO service_requests 
    (driver_id, company_id, car_type, service_lat, service_lng)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['driver_id'],
        mechanic['company_id'],
        data['car_type'],
        data['service_lat'],
        data['service_lng']
    ))
    connection.commit()
    cursor.close()
    connection.close()



def assign_mechanic_to_request(request_id, mechanic_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """
    UPDATE service_requests 
    SET mechanic_id = %s, request_status = 'assigned' 
    WHERE id = %s
    """
    cursor.execute(sql, (mechanic_id, request_id))
    connection.commit()
    cursor.close()
    connection.close()


def get_available_mechanic(car_type, service_lat, service_lng):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get all available mechanics who match the car type
    sql = """
    SELECT id, company_id, name, mechanic_latitude, mechanic_longitude, specialties
    FROM mechanics
    WHERE is_available = 1 AND specialties LIKE %s
    """
    cursor.execute(sql, (f"%{car_type}%",))
    mechanics = cursor.fetchall()

    if not mechanics:
        return None

    # Find nearest mechanic based on simple distance (Haversine formula not used here for simplicity)
    def calculate_distance(lat1, lng1, lat2, lng2):
        return math.sqrt((lat1 - lat2)**2 + (lng1 - lng2)**2)

    nearest_mechanic = min(
        mechanics,
        key=lambda mech: calculate_distance(
            float(service_lat),
            float(service_lng),
            float(mech['mechanic_latitude']),
            float(mech['mechanic_longitude'])
        )
    )

    cursor.close()
    connection.close()
    return nearest_mechanic

def update_mechanic_location(request_id, latitude, longitude):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """
    UPDATE service_requests
    SET mechanic_latitude = %s, mechanic_longitude = %s
    WHERE id = %s
    """
    cursor.execute(sql, (latitude, longitude, request_id))
    connection.commit()
    cursor.close()
    connection.close()


def get_mechanic_location(request_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """
    SELECT mechanic_latitude, mechanic_longitude
    FROM service_requests
    WHERE id = %s
    """
    cursor.execute(sql, (request_id,))
    location = cursor.fetchone()
    cursor.close()
    connection.close()
    return location  # returns (latitude, longitude) tuple or None
