from clases.asignacion_empleado_habitacion import AsignacionEmpleadoHabitacion


class AsignacionEmpleadoHabRepository:
    def __init__(self, db):
        self.db = db

    def create(self, asignacion):
        conn = self.db.get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO empleados_habitaciones (empleado_id, habitacion_numero, fecha_asignacion, tarea) VALUES (?, ?, ?, ?)',
                       (asignacion.empleado_id, asignacion.habitacion_numero, asignacion.fecha_asignacion, asignacion.tarea))
        conn.commit()
        return cursor.lastrowid

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id_asignacion, empleado_id, habitacion_numero, fecha_asignacion, tarea FROM empleados_habitaciones")
        asignaciones_data = cursor.fetchall()

        asignaciones = [AsignacionEmpleadoHabitacion(id_asignacion=data[0], empleado_id=data[1], habitacion_numero=data[2], fecha_asignacion=data[3], tarea=data[4])
                        for data in asignaciones_data]

        return asignaciones