from clases.asignacion_empleado_habitacion import AsignacionEmpleadoHabitacion
from repositories.asignacion_empleado_hab_repository import AsignacionEmpleadoHabRepository
from repositories.empleado_repository import EmpleadoRepository


class EmpleadoService:
    def __init__(self, db):
        self.empleado_repository = EmpleadoRepository(db)
        self.asignacion_empleado_hab_repository = AsignacionEmpleadoHabRepository(db)

    def get_all(self):
        return self.empleado_repository.get_all()

    def create_asignacion(self, asignacion):
        asignacion = AsignacionEmpleadoHabitacion(
            empleado_id=asignacion['empleado'],
            habitacion_numero=asignacion['habitacion'],
            fecha_asignacion=asignacion['fecha_asignacion'],
            tarea=asignacion['tarea']
        )
        return self.asignacion_empleado_hab_repository.create(asignacion)

    def get_by_id(self, id):
        return self.empleado_repository.get_by_id(id)

    def get_all_asignaciones(self):
        return self.asignacion_empleado_hab_repository.get_all()