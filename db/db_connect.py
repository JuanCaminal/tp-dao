import os
from sqlite3 import connect


class DBConnect:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            db_path = os.path.join('db', 'hotel.db')
            cls.__instance.db = connect(db_path)
            cls.__instance.crear_tablas()  # Llamamos al método que crea las tablas si no existen
        return cls.__instance

    def get_db(self):
        return self.db

    def cursor(self):
        return self.db.cursor()

    def close_db(self):
        self.db.close()

    def crear_tablas(self):
        cursor = self.db.cursor()
        
        # Crear tablas (método anterior)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                email TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleado (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cargo TEXT,
                sueldo REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitacion (
                numero INTEGER PRIMARY KEY,
                tipo TEXT NOT NULL,
                estado TEXT,
                precio_por_noche REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reserva (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                habitacion_numero INTEGER,
                fecha_entrada TEXT,
                fecha_salida TEXT,
                cantidad_personas INTEGER,
                FOREIGN KEY(cliente_id) REFERENCES cliente(id_cliente),
                FOREIGN KEY(habitacion_numero) REFERENCES habitacion(numero)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS factura (
                id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                reserva_id INTEGER,
                fecha_emision TEXT,
                total REAL,
                FOREIGN KEY(cliente_id) REFERENCES cliente(id_cliente),
                FOREIGN KEY(reserva_id) REFERENCES reserva(id_reserva)
            )
        """)
        self.db.commit()