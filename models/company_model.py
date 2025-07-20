from db_config import get_db_connection

def create_company(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """
    INSERT INTO companies (company_name, email, phone, password)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['company_name'],
        data['email'],
        data['phone'],
        data['password']
    ))
    connection.commit()
    cursor.close()
    connection.close()

def get_company_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM companies WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

