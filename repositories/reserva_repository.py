from clases.reserva import Reserva
from datetime import datetime

class ReservaRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id_reserva, cliente_id, habitacion_numero, fecha_entrada, fecha_salida, cantidad_personas FROM reservas")
        reservas_data = cursor.fetchall()

        # Transformar las tuplas en objetos Reserva
        reservas = [Reserva(id_reserva=data[0], cliente=data[1], habitacion=data[2], fecha_entrada=data[3], fecha_salida=data[4], cantidad_personas=data[5])
                    for data in reservas_data]

        return reservas

    def get_by_id(self, id):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reservas WHERE id_reserva = ?', (id,))
        reserva_data = cursor.fetchone()
        reserva = Reserva(id_reserva=reserva_data[0], cliente=reserva_data[1], habitacion=reserva_data[2], fecha_entrada=reserva_data[3], fecha_salida=reserva_data[4], cantidad_personas=reserva_data[5])

        return reserva

    def get_by_date_range(self, fecha_inicio, fecha_fin):
        cursor = self.db.cursor()
        query = """
            SELECT id_reserva, cliente_id, habitacion_numero, fecha_entrada, fecha_salida, cantidad_personas 
            FROM reservas 
            WHERE fecha_entrada >= ? AND fecha_salida <= ?
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        reservas_data = cursor.fetchall()

        # Transformar los resultados en objetos Reserva
        reservas = [
            Reserva(
                id_reserva=data[0],
                cliente=data[1],
                habitacion=data[2],
                fecha_entrada=data[3],
                fecha_salida=data[4],
                cantidad_personas=data[5]
            )
            for data in reservas_data
        ]

        return reservas

    def get_reserva_chek_in_out(self, id_reserva=None):
        cursor = self.db.cursor()
        fecha_actual = datetime.now().date().strftime("%Y-%m-%d")  # Obtener la fecha de hoy

        # Consulta SQL para incluir el estado de la habitación
        query = """
                    SELECT 
                        r.id_reserva, 
                        c.nro_documento AS dni_cliente, 
                        r.habitacion_numero, 
                        r.fecha_entrada, 
                        r.fecha_salida, 
                        r.cantidad_personas,
                        h.estado AS estado_habitacion
                    FROM reservas r
                    INNER JOIN clientes c ON r.cliente_id = c.id_cliente
                    INNER JOIN habitaciones h ON r.habitacion_numero = h.numero
                    WHERE ? BETWEEN 
              (substr(r.fecha_entrada, 7, 4) || '-' || substr(r.fecha_entrada, 4, 2) || '-' || substr(r.fecha_entrada, 1, 2)) AND 
              (substr(r.fecha_salida, 7, 4) || '-' || substr(r.fecha_salida, 4, 2) || '-' || substr(r.fecha_salida, 1, 2))
                """
        params = [fecha_actual]

        # Agregar filtro opcional por id_reserva
        if id_reserva:
            query += " AND r.id_reserva = ?"
            params.append(id_reserva)

        cursor.execute(query, params)
        reservas_data = cursor.fetchall()

        # Crear lista de reservas junto con el estado de la habitación
        reservas = [
            (Reserva(
                id_reserva=data[0],
                cliente=data[1],  # DNI del cliente
                habitacion=data[2],
                fecha_entrada=data[3],
                fecha_salida=data[4],
                cantidad_personas=data[5]
            ), data[6])  # data[6] es el estado de la habitación
            for data in reservas_data
        ]

        return reservas

    def create(self, reserva):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reservas (cliente_id, habitacion_numero, fecha_entrada, fecha_salida, cantidad_personas) VALUES (?, ?, ?, ?, ?)',
                       (reserva.cliente, reserva.habitacion, reserva.fecha_entrada, reserva.fecha_salida, reserva.cantidad_personas))
        conn.commit()
        return cursor.lastrowid

    def update(self, id, reserva):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE reservas SET cliente_id = ?, habitacion_numero = ?, fecha_entrada = ?, fecha_salida = ?, cantidad_personas = ? WHERE id_reserva = ?',
                       (reserva.cliente, reserva.habitacion, reserva.fecha_entrada, reserva.fecha_salida, reserva.cantidad_personas, id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, id):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reservas WHERE id_reserva = ?', (id,))
        self.db.commit()
        return cursor.rowcount