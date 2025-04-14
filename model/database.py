import psycopg2 # type: ignore

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
            print("Conexión exitosa a la base de datos")
        except Exception as e:
            print("Error al conectar a la base de datos:", e)
            self.connection = None
        self.cursor = self.connection.cursor() if self.connection else None