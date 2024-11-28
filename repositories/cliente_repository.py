from clases.cliente import Cliente


class ClienteRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT id_cliente, nro_documento, nombre, apellido, direccion, telefono, email, puntos_fidelizacion, puntos_fidelizacion_canjeados FROM clientes")
        clientes_data = cursor.fetchall()

        # Transformar las tuplas en objetos Cliente
        clientes = [
            Cliente(id_cliente=data[0], nro_documento=data[1], nombre=data[2], apellido=data[3], direccion=data[4],
                    telefono=data[5], email=data[6], puntos_fidelizacion=data[7], puntos_fidelizacion_canjeados=data[8])
            for data in clientes_data]

        return clientes


    def get_by_id(self, id):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id_cliente = ?', (id,))
        cliente_data = cursor.fetchone()
        cliente = Cliente(id_cliente=cliente_data[0], nro_documento=cliente_data[1], nombre=cliente_data[2],
                          apellido=cliente_data[3], direccion=cliente_data[4], telefono=cliente_data[5],
                          email=cliente_data[6], puntos_fidelizacion=cliente_data[7],
                          puntos_fidelizacion_canjeados=cliente_data[8])

        return cliente

    def get_by_dni(self, dni):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE nro_documento = ?', (dni,))
        cliente_data = cursor.fetchone()
        cliente = Cliente(id_cliente=cliente_data[0], nro_documento=cliente_data[1], nombre=cliente_data[2],
                          apellido=cliente_data[3], direccion=cliente_data[4], telefono=cliente_data[5],
                          email=cliente_data[6], puntos_fidelizacion=cliente_data[7],
                          puntos_fidelizacion_canjeados=cliente_data[8])

        return cliente


    def create(self, cliente):
        query = """
        INSERT INTO clientes (nombre, apellido, direccion, telefono, email, nro_documento, puntos_fidelizacion, puntos_fidelizacion_canjeados)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            cliente.nombre,  # Accede al atributo usando el getter
            cliente.apellido,
            cliente.direccion,
            cliente.telefono,
            cliente.email,
            cliente.nro_documento,
            cliente.puntos_fidelizacion,
            cliente.puntos_fidelizacion_canjeados
        )
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        return cursor.lastrowid

    def update(self, id, cliente):
        cursor = self.db.cursor()
        cursor.execute("""
                        UPDATE clientes
                        SET nombre = ?, apellido = ?, direccion = ?, telefono = ?, email = ?, nro_documento = ?, puntos_fidelizacion = ?, puntos_fidelizacion_canjeados = ?
                        WHERE id_cliente = ?
                        """,
                       (cliente.nombre, cliente.apellido, cliente.dni, cliente.telefono, cliente.email, id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, id):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM clientes WHERE id_cliente = ?', (id,))
        self.db.commit()
        return cursor.rowcount

    def get_puntos(self, id_cliente):
        cursor = self.db.cursor()
        query = "SELECT puntos_fidelizacion FROM clientes WHERE nro_documento = ?"
        cursor.execute(query, (id_cliente,))
        result = cursor.fetchone()
        return result[0] if result else 0

    def actualizar_puntos(self, id_cliente, puntos):
        cursor = self.db.cursor()
        query = "UPDATE clientes SET puntos_fidelizacion = ? WHERE nro_documento = ?"
        cursor.execute(query, (puntos, id_cliente))
        self.db.commit()

    def get_puntos_canjeados(self, id_cliente):
        cursor = self.db.cursor()
        query = "SELECT puntos_fidelizacion_canjeados FROM clientes WHERE nro_documento = ?"
        cursor.execute(query, (id_cliente,))
        result = cursor.fetchone()
        return result[0] if result else 0

    def actualizar_puntos_canjeados(self, id_cliente, puntos):
        cursor = self.db.cursor()
        query = "UPDATE clientes SET puntos_fidelizacion_canjeados = ? WHERE nro_documento = ?"
        cursor.execute(query, (puntos, id_cliente))
        self.db.commit()