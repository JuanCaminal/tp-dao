from clases.factura import Factura


class FacturaRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id_factura, cliente_id, reserva_id, fecha_emision, total
            FROM factura
        """)
        facturas_data = cursor.fetchall()

        # Transformar las tuplas en objetos Factura
        facturas = [
            Factura(
                id_factura=data[0],
                cliente=data[1],
                reserva=data[2],
                fecha_emision=data[3],
                total=data[4]
            )
            for data in facturas_data
        ]

        return facturas

    def get_by_id(self, id_factura):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id_factura, cliente_id, reserva_id, fecha_emision, total
            FROM factura
            WHERE id_factura = ?
        """, (id_factura,))
        factura_data = cursor.fetchone()

        if factura_data is None:
            return None

        # Crear y devolver un objeto Factura
        return Factura(
            id_factura=factura_data[0],
            cliente=factura_data[1],
            reserva=factura_data[2],
            fecha_emision=factura_data[3],
            total=factura_data[4]
        )

    def create(self, factura):
        query = """
        INSERT INTO factura (cliente_id, reserva_id, fecha_emision, total)
        VALUES (?, ?, ?, ?)
        """
        values = (
            factura.cliente,
            factura.reserva,
            factura.fecha_emision,
            factura.total
        )
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        return cursor.lastrowid

    def update(self, id_factura, factura):
        query = """
        UPDATE factura
        SET cliente_id = ?, reserva_id = ?, fecha_emision = ?, total = ?
        WHERE id_factura = ?
        """
        values = (
            factura.cliente_id,
            factura.reserva_id,
            factura.fecha_emision,
            factura.total,
            id_factura
        )
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        return cursor.rowcount

    def delete(self, id_factura):
        query = "DELETE FROM factura WHERE id_factura = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (id_factura,))
        self.db.commit()
        return cursor.rowcount
