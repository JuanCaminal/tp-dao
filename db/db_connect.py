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

    def commit(self):
        """Método para hacer commit a la base de datos."""
        self.db.commit()  # Asegúrate de llamar al commit sobre la conexión a la base de datos.

    def crear_tablas(self):
        cursor = self.db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nro_documento TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                email TEXT,
                puntos_fidelizacion INTEGER DEFAULT 0
            )
        """)

        # Tabla de empleados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cargo TEXT,
                sueldo REAL
            )
        """)
        # Tabla de habitaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitaciones (
                numero INTEGER PRIMARY KEY,
                tipo TEXT CHECK(tipo IN ('Simple', 'Doble', 'Suite')) NOT NULL,
                estado TEXT CHECK(estado IN ('Disponible', 'Ocupada')) NOT NULL,
                precio_por_noche REAL
            )
        """)
        # Tabla de reservas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                habitacion_numero INTEGER,
                fecha_entrada TEXT,
                fecha_salida TEXT,
                cantidad_personas INTEGER,
                FOREIGN KEY(cliente_id) REFERENCES clientes(id_cliente),
                FOREIGN KEY(habitacion_numero) REFERENCES habitaciones(numero)
            )
        """)
        # Tabla de facturas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS factura (
                id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                reserva_id INTEGER,
                fecha_emision TEXT,
                total REAL,
                FOREIGN KEY(cliente_id) REFERENCES clientes(id_cliente),
                FOREIGN KEY(reserva_id) REFERENCES reservas(id_reserva)
            )
        """)
        # Nueva tabla para asignar empleados a habitaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados_habitaciones (
                id_asignacion INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER,
                habitacion_numero INTEGER,
                fecha_asignacion TEXT,
                tarea TEXT,
                FOREIGN KEY(empleado_id) REFERENCES empleados(id_empleado),
                FOREIGN KEY(habitacion_numero) REFERENCES habitaciones(numero)
            )
        """)
        # Confirmar los cambios
        self.db.commit()
