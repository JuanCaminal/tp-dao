from clases.reserva import Reserva

class ReservaRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id_reserva, cliente_id, habitacion_numero, fecha_entrada, fecha_salida, cantidad_personas FROM reservas")
        reservas_data = cursor.fetchall()

        # Transformar las tuplas en objetos Reserva
        reservas = [Reserva(id_reserva=data[0], cliente=data[1], habitacion=data[2], fecha_entrada=data[3], fecha_salida=data[4], cantidad_personas=data[5]) for data
                    in
                    reservas_data]

        return reservas

    def get_by_id(self, id):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reservas WHERE id_reserva = ?', (id,))
        reserva_data = cursor.fetchone()
        reserva = Reserva(id_reserva=reserva_data[0], cliente=reserva_data[1], habitacion=reserva_data[2], fecha_entrada=reserva_data[3], fecha_salida=reserva_data[4], cantidad_personas=reserva_data[5])

        return reserva

    def create(self, reserva):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reservas (cliente_id, habitacion_numero, fecha_entrada, fecha_salida, cantidad_personas) VALUES (?, ?, ?, ?, ?)',
                       (reserva.cliente, reserva.habitacion, reserva.fecha_entrada, reserva.fecha_salida, reserva.cantidad_personas))
        conn.commit()
        return cursor.lastrowid

    def update(self, id, reserva):
        cursor = self.db.cursor()
        cursor.execute('UPDATE reservas SET cliente_id = ?, habitacion_numero = ?, fecha_entrada = ?, fecha_salida = ?, cantidad_personas = ? WHERE id_reserva = ?',
                       (reserva.cliente, reserva.habitacion, reserva.fecha_entrada, reserva.fecha_salida, reserva.cantidad_personas, id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, id):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM reservas WHERE id_reserva = ?', (id,))
        self.db.commit()
        return cursor.rowcount