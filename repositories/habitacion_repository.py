from clases.habitacion import Habitacion

class HabitacionRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT numero, tipo, estado, precio_por_noche FROM habitaciones")
        habitaciones_data = cursor.fetchall()

        # Transformar las tuplas en objetos Habitacion
        habitaciones = [Habitacion(numero=data[0], tipo=data[1], estado=data[2], precio_por_noche=data[3]) for data in habitaciones_data]

        return habitaciones

    def get_by_id(self, numero):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitaciones WHERE numero = ?', (numero,))
        habitacion_data = cursor.fetchone()
        habitacion = Habitacion(numero=habitacion_data[0], tipo=habitacion_data[1], estado=habitacion_data[2], precio_por_noche=habitacion_data[3])

        return habitacion

    def create(self, habitacion):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO habitaciones (numero, tipo, estado, precio_por_noche) VALUES (?, ?, ?, ?)',
                       (habitacion.numero, habitacion.tipo, habitacion.estado, habitacion.precio_por_noche))
        conn.commit()
        return cursor.lastrowid

    def update(self, numero, habitacion):
        cursor = self.db.cursor()
        cursor.execute('UPDATE habitaciones SET tipo = ?, estado = ?, precio_por_noche = ? WHERE numero = ?',
                       (habitacion.tipo, habitacion.estado, habitacion.precio_por_noche, numero))
        self.db.commit()
        return cursor.rowcount

    def delete(self, numero):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM habitaciones WHERE numero = ?', (numero,))
        self.db.commit()
        return cursor.rowcount

    def get_diponibles_by_date_range(self, fecha_entrada, fecha_salida):
        cursor = self.db.cursor()
        query = """
            SELECT numero, tipo, estado, precio_por_noche
            FROM habitaciones
            WHERE numero NOT IN (
                SELECT habitacion_numero
                FROM reservas
                WHERE (
                    (fecha_entrada <= ? AND fecha_salida >= ?) OR
                    (fecha_entrada <= ? AND fecha_salida >= ?) OR
                    (fecha_entrada >= ? AND fecha_salida <= ?)
                )
            );
        """
        cursor.execute(query, (fecha_salida, fecha_entrada, fecha_salida, fecha_entrada, fecha_entrada, fecha_salida))
        habitaciones_data = cursor.fetchall()

        # Transformar los resultados en objetos Habitacion
        habitaciones_disponibles = [
            Habitacion(
                numero=data[0],
                tipo=data[1],
                estado=data[2],
                precio_por_noche=data[3]
            )
            for data in habitaciones_data
        ]

        return habitaciones_disponibles