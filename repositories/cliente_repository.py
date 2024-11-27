from clases.cliente import Cliente


class ClienteRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id_cliente, nombre, apellido, direccion, telefono, email, nro_documento FROM clientes")
        clientes_data = cursor.fetchall()

        # Transformar las tuplas en objetos Cliente
        clientes = [Cliente(id_cliente=data[0], nombre=data[1], apellido=data[2], direccion=data[3], telefono=data[4],
                            email=data[5], nro_documento=data[6]) for data in clientes_data]

        return clientes

    def get_by_id(self, id):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id_cliente = ?', (id,))
        cliente_data = cursor.fetchone()
        cliente = Cliente(id_cliente=cliente_data[0], nombre=cliente_data[1], apellido=cliente_data[2],direccion=cliente_data[3],telefono=cliente_data[4], email=cliente_data[5])

        return cliente

    def create(self, cliente):
        query = """
        INSERT INTO clientes (nombre, apellido, direccion, telefono, email, nro_documento)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (
            cliente.nombre,         # Accede al atributo usando el getter
            cliente.apellido,
            cliente.direccion,
            cliente.telefono,
            cliente.email,
            cliente.nro_documento
        )
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        return cursor.lastrowid

    def update(self, id, cliente):
        cursor = self.db.cursor()
        cursor.execute('UPDATE clientes SET nombre = ?, apellido = ?, dni = ?, telefono = ?, email = ? WHERE id_cliente = ?',
                       (cliente.nombre, cliente.apellido, cliente.dni, cliente.telefono, cliente.email, id))
        self.db.commit()
        return cursor.rowcount

    def delete(self, id):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM clientes WHERE id_cliente = ?', (id,))
        self.db.commit()
        return cursor.rowcount
