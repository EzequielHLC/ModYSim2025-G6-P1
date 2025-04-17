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
        self.create_tables()

    def create_tables(self):
        if self.cursor:
            try:
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS vn_results (
                    id SERIAL PRIMARY KEY,
                    seed INTEGER NOT NULL,
                    random_numbers TEXT NOT NULL,
                    chi_square_result BOOLEAN,
                    rachas_result BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS mixed_congruence_results (
                    id SERIAL PRIMARY KEY,
                    seed INTEGER NOT NULL,
                    a INTEGER NOT NULL,
                    m INTEGER NOT NULL,
                    c INTEGER NOT NULL,
                    random_numbers TEXT NOT NULL,
                    chi_square_result BOOLEAN,
                    rachas_result BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                self.connection.commit()
            except Exception as e:
                message_box.MessageBox.show_error("Error al crear tablas", f"No se pudieron crear las tablas: {e}")
                self.connection.rollback()
    
    def execute(self, query, params=None):
        if self.cursor:
            try:
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                return True
            except Exception as e:
                message_box.MessageBox.show_error("Error al ejecutar consulta", f"No se pudo ejecutar la consulta: {e}")
                return False
        return False