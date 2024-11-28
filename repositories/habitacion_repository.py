from clases.habitacion import Habitacion
from datetime import datetime

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

        # Convertimos las fechas a formato 'YYYY-MM-DD' para trabajar con las reservas en la base de datos
        fecha_entrada = datetime.strptime(fecha_entrada, '%d/%m/%Y').strftime('%Y-%m-%d')
        fecha_salida = datetime.strptime(fecha_salida, '%d/%m/%Y').strftime('%Y-%m-%d')

        # Consulta para obtener las habitaciones que están reservadas en el rango de fechas especificado
        query = """
            SELECT r.habitacion_numero, r.fecha_entrada, r.fecha_salida
            FROM reservas r
            WHERE ? BETWEEN 
                (substr(r.fecha_entrada, 7, 4) || '-' || substr(r.fecha_entrada, 4, 2) || '-' || substr(r.fecha_entrada, 1, 2)) 
                AND (substr(r.fecha_salida, 7, 4) || '-' || substr(r.fecha_salida, 4, 2) || '-' || substr(r.fecha_salida, 1, 2))
            OR ? BETWEEN 
                (substr(r.fecha_entrada, 7, 4) || '-' || substr(r.fecha_entrada, 4, 2) || '-' || substr(r.fecha_entrada, 1, 2)) 
                AND (substr(r.fecha_salida, 7, 4) || '-' || substr(r.fecha_salida, 4, 2) || '-' || substr(r.fecha_salida, 1, 2))
            OR (? BETWEEN 
                (substr(r.fecha_entrada, 7, 4) || '-' || substr(r.fecha_entrada, 4, 2) || '-' || substr(r.fecha_entrada, 1, 2)) 
                AND (substr(r.fecha_salida, 7, 4) || '-' || substr(r.fecha_salida, 4, 2) || '-' || substr(r.fecha_salida, 1, 2)))
        """
        cursor.execute(query, (fecha_entrada, fecha_salida, fecha_entrada))
        reservas_data = cursor.fetchall()

        # Agrupamos las reservas por habitación
        reservas_por_habitacion = {}
        for reserva in reservas_data:
            habitacion_numero = reserva[0]
            fecha_entrada_reserva = reserva[1]
            fecha_salida_reserva = reserva[2]
            if habitacion_numero not in reservas_por_habitacion:
                reservas_por_habitacion[habitacion_numero] = []
            reservas_por_habitacion[habitacion_numero].append((fecha_entrada_reserva, fecha_salida_reserva))

        # Obtener todas las habitaciones
        query_habitaciones = """
            SELECT numero, tipo, estado, precio_por_noche
            FROM habitaciones;
        """
        cursor.execute(query_habitaciones)
        habitaciones_data = cursor.fetchall()

        # Lista para almacenar los lapsos de disponibilidad por cada habitación
        lapsos_disponibilidad = []

        # Comprobamos los lapsos disponibles por cada habitación
        for habitacion in habitaciones_data:
            habitacion_numero = habitacion[0]
            estado = habitacion[2]

            # Solo verificamos habitaciones en estado 'Disponible'
            if estado != "Disponible":
                continue

            # Verificamos las reservas de la habitación
            if habitacion_numero in reservas_por_habitacion:
                reservas = reservas_por_habitacion[habitacion_numero]

                # Ordenamos las reservas por fecha de entrada
                reservas.sort(key=lambda x: x[0])

                # Definir los lapsos disponibles (inicialmente asumiendo disponibilidad completa)
                lapsos = []

                # Verificar si hay disponibilidad antes de la primera reserva
                if reservas[0][0] > fecha_entrada:
                    lapsos.append((fecha_entrada, reservas[0][0]))

                # Verificar los lapsos entre reservas
                for i in range(1, len(reservas)):
                    if reservas[i][0] > reservas[i - 1][1]:
                        lapsos.append((reservas[i - 1][1], reservas[i][0]))

                # Verificar si hay disponibilidad después de la última reserva
                if reservas[-1][1] < fecha_salida:
                    lapsos.append((reservas[-1][1], fecha_salida))

                # Agregar los lapsos encontrados
                lapsos_disponibilidad.append((habitacion_numero, lapsos))

            else:
                # Si la habitación no tiene reservas, está completamente disponible
                lapsos_disponibilidad.append((habitacion_numero, [(fecha_entrada, fecha_salida)]))

        return lapsos_disponibilidad
