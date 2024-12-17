import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Загрузка переменных из .env
load_dotenv()

def get_connection():
    """
    Создает подключение к базе данных PostgreSQL.
    Возвращает объект соединения.
    """
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            cursor_factory=RealDictCursor  # Формат результата: словарь
        )
        return connection
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise

def test_connection():
    """
    Тестирует подключение к базе данных и выводит список таблиц.
    """
    connection = get_connection()
    if connection:
        print("Подключение успешно!")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cursor.fetchall()
                print("Список таблиц в базе данных:")
                for table in tables:
                    print(table["table_name"])
        except psycopg2.Error as e:
            print(f"Ошибка выполнения SQL-запроса: {e}")
        finally:
            connection.close()

