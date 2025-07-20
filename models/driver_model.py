from db_config import get_db_connection

def create_driver(data):
    connection = get_db_connection()  # ✅ Correctly calls the function to get a connection
    cursor = connection.cursor()
    sql = """
    INSERT INTO drivers (full_name, national_id, number_plate, car_type, phone, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['full_name'],
        data['national_id'],
        data['number_plate'],
        data['car_type'],
        data['phone'],
        data['password']
    ))
    connection.commit()
    cursor.close()
    connection.close()


def get_driver_by_phone(phone):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM drivers WHERE phone = %s", (phone,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result
    