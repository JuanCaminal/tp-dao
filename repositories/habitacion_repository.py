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

        if habitacion_data is None:
            return None
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
        conn = self.db.get_db()  # Asegúrate de obtener la conexión correctamente
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE habitaciones SET tipo = ?, estado = ?, precio_por_noche = ? WHERE numero = ?',
            (habitacion.tipo, habitacion.estado, habitacion.precio_por_noche, numero)
        )
        conn.commit()
        return cursor.rowcount

        # cursor = self.db.cursor()
        # cursor.execute('UPDATE habitaciones SET tipo = ?, estado = ?, precio_por_noche = ? WHERE numero = ?',
        #                (habitacion.tipo, habitacion.estado, habitacion.precio_por_noche, numero))
        # self.db.commit()
        # return cursor.rowcount

    def delete(self, numero):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM habitaciones WHERE numero = ?', (numero,))
        self.db.commit()
        return cursor.rowcount

    def get_diponibles_by_date_range(self, fecha_entrada, fecha_salida):
        cursor = self.db.cursor()
        query = """
            WITH RangoConsultado AS (
    SELECT 
        ? AS fecha_inicio, 
        ? AS fecha_fin
),
ReservasOrdenadas AS (
    SELECT 
        habitacion_numero, 
        fecha_entrada, 
        fecha_salida
    FROM reservas
    WHERE fecha_salida >= (SELECT fecha_inicio FROM RangoConsultado)
      AND fecha_entrada <= (SELECT fecha_fin FROM RangoConsultado)
),
FechasDisponibles AS (
    SELECT 
        h.numero,
        h.tipo,
        h.estado,
        h.precio_por_noche,
        COALESCE(MAX(r.fecha_salida), (SELECT fecha_inicio FROM RangoConsultado)) AS fecha_inicio_disponible,
        COALESCE(MIN(r2.fecha_entrada), (SELECT fecha_fin FROM RangoConsultado)) AS fecha_fin_disponible
    FROM habitaciones h
    LEFT JOIN ReservasOrdenadas r ON h.numero = r.habitacion_numero
    LEFT JOIN ReservasOrdenadas r2 ON h.numero = r2.habitacion_numero AND r2.fecha_entrada > r.fecha_salida
    WHERE h.estado = 'Disponible'
    GROUP BY h.numero, h.tipo, h.estado, h.precio_por_noche
)
SELECT 
    numero, 
    tipo, 
    estado, 
    precio_por_noche, 
    CASE 
        WHEN fecha_inicio_disponible > (SELECT fecha_inicio FROM RangoConsultado) THEN fecha_inicio_disponible
        ELSE (SELECT fecha_inicio FROM RangoConsultado)
    END AS fecha_disponible_desde,
    CASE 
        WHEN fecha_fin_disponible < (SELECT fecha_fin FROM RangoConsultado) THEN fecha_fin_disponible
        ELSE (SELECT fecha_fin FROM RangoConsultado)
    END AS fecha_disponible_hasta
FROM FechasDisponibles
WHERE fecha_inicio_disponible < fecha_fin_disponible
ORDER BY numero, fecha_disponible_desde;


        """
        cursor.execute(query, (fecha_entrada, fecha_salida))
        habitaciones_data = cursor.fetchall()

        # Crear objetos Habitacion con información adicional sobre la disponibilidad
        habitaciones_disponibles = [
            {
                "habitacion": Habitacion(
                    numero=data[0],
                    tipo=data[1],
                    estado=data[2],
                    precio_por_noche=data[3]
                ),
                "fecha_disponible_desde": data[4],
                "fecha_disponible_hasta": data[5]
            }
            for data in habitaciones_data
        ]
        return habitaciones_disponibles