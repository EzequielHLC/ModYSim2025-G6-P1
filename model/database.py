import psycopg2
from view import message_box

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="RandomNumbersDB",
            user="postgres",
            password="magna"
            )
        except Exception as e:
            message_box.MessageBox.show_error("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            self.connection = None
        self.cursor = self.connection.cursor() if self.connection else None