import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения из .env файла


class Database:
    def __init__(self):
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASS = os.getenv('DB_PASS')
        self.DB_PORT = os.getenv('DB_PORT')

        self.connection = psycopg2.connect(
            host=self.DB_HOST,
            port=self.DB_PORT,
            dbname=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASS
        )
        self.cursor = self.connection.cursor()

    def insert_image(self, title, image_path, image_size, description, tags, extension):
        self.cursor.execute('''
                        INSERT INTO images (title, path, size, description, tags, extension)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (title, image_path, image_size, description, tags, extension))

        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
