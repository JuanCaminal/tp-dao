from clases.empleado import Empleado


class EmpleadoRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id_empleado, nombre, apellido, cargo, sueldo FROM empleados")
        empleados_data = cursor.fetchall()

        empleados = [Empleado(id_empleado=data[0], nombre=data[1], apellido=data[2], cargo=data[3], sueldo=data[4])
                     for data in empleados_data]

        return empleados

    def get_by_id(self, id):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM empleados WHERE id_empleado = ?', (id,))
        empleado_data = cursor.fetchone()
        empleado = Empleado(id_empleado=empleado_data[0], nombre=empleado_data[1], apellido=empleado_data[2], cargo=empleado_data[3], sueldo=empleado_data[4])

        return empleado