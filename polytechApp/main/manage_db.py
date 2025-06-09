import psycopg2
from psycopg2 import Error

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="cursach",
            user="postgres",
            password="LAPTOPsupremacy1!",
            port="5432"
        )
        return connection
    except Error as e:
        print(f"Ошибка при подключении:: {e}")
        return None

def setup_database():
    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor()

    with open('polytechDB.sql', 'r') as file:
        sql_script = file.read()
        try:
            cursor.execute(sql_script)
            connection.commit()
            print("База данных успешно настроена.")
        except Error as e:
            print(f"Ошибка при выполнении SQL-скрипта: {e}")
            connection.rollback()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    setup_database()