from clases.cliente import Cliente


class ClienteRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT id_cliente, nombre, apellido, direccion, telefono, email, nro_documento, puntos_fidelizacion FROM clientes")
        clientes_data = cursor.fetchall()

        # Transformar las tuplas en objetos Cliente
        clientes = [
            Cliente(
                id_cliente=data[0],
                nombre=data[1],
                apellido=data[2],
                direccion=data[3],
                telefono=data[4],
                email=data[5],
                nro_documento=data[6],
                puntos_fidelizacion=data[7]
            )
            for data in clientes_data
        ]

        return clientes

    def get_by_id(self, id):
        conn = self.db
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id_cliente, nombre, apellido, direccion, telefono, email, nro_documento, puntos_fidelizacion FROM clientes WHERE id_cliente = ?',
            (id,))
        cliente_data = cursor.fetchone()

        if cliente_data:
            cliente = Cliente(
                id_cliente=cliente_data[0],
                nombre=cliente_data[1],
                apellido=cliente_data[2],
                direccion=cliente_data[3],
                telefono=cliente_data[4],
                email=cliente_data[5],
                nro_documento=cliente_data[6],
                puntos_fidelizacion=cliente_data[7]
            )
            return cliente
        return None

    def create(self, cliente):
        query = """
        INSERT INTO clientes (nombre, apellido, direccion, telefono, email, nro_documento, puntos_fidelizacion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            cliente.nombre,
            cliente.apellido,
            cliente.direccion,
            cliente.telefono,
            cliente.email,
            cliente.nro_documento,
            cliente.puntos_fidelizacion
        )
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        return cursor.lastrowid

    def update(self, id, cliente):
        query = """
        UPDATE clientes
        SET nombre = ?, apellido = ?, direccion = ?, telefono = ?, email = ?, nro_documento = ?, puntos_fidelizacion = ?
        WHERE id_cliente = ?
        """
        values = (
            cliente.nombre,
            cliente.apellido,
            cliente.direccion,
            cliente.telefono,
            cliente.email,
            cliente.nro_documento,
            cliente.puntos_fidelizacion,
            id
        )
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        return cursor.rowcount

    def delete(self, id):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM clientes WHERE id_cliente = ?', (id,))
        self.db.commit()
        return cursor.rowcount

    def get_puntos(self, id_cliente):
        cursor = self.db.cursor()
        query = "SELECT puntos_fidelizacion FROM clientes WHERE id_cliente = ?"
        cursor.execute(query, (id_cliente,))
        result = cursor.fetchone()
        return result[0] if result else 0

    def actualizar_puntos(self, id_cliente, puntos):
        cursor = self.db.cursor()
        query = "UPDATE clientes SET puntos_fidelizacion = ? WHERE id_cliente = ?"
        cursor.execute(query, (puntos, id_cliente))
        self.db.commit()
