from db_config import get_db_connection

def create_service_request(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """
    INSERT INTO service_requests 
    (driver_id, company_id, car_type, service_lat, service_lng)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['driver_id'],
        data['company_id'],
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


def get_available_mechanic(company_id, car_type):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """
    SELECT * FROM mechanics 
    WHERE company_id = %s AND is_available = 1 AND specialties LIKE %s
    LIMIT 1
    """
    cursor.execute(sql, (company_id, f"%{car_type}%"))
    mechanic = cursor.fetchone()
    cursor.close()
    connection.close()
    return mechanic

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
