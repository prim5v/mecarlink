from db_config import get_db_connection

def update_mechanic_availability(mechanic_id, availability):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE mechanics SET is_available = %s WHERE id = %s", (availability, mechanic_id))
    connection.commit()
    cursor.close()
    connection.close()

def update_mechanic_location(mechanic_id, lat, lng):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE mechanics SET current_lat = %s, current_lng = %s WHERE id = %s",
        (lat, lng, mechanic_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

def get_mechanic_location(mechanic_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT current_lat, current_lng FROM mechanics WHERE id = %s",
        (mechanic_id,)
    )
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result
