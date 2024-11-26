class AsignacionEmpleadoHabitacion:
    def __init__(self, empleado_id, habitacion_numero, fecha_asignacion, tarea, id_asignacion=None):
        self._id_asignacion = id_asignacion
        self._empleado_id = empleado_id
        self._habitacion_numero = habitacion_numero
        self._fecha_asignacion = fecha_asignacion
        self._tarea = tarea

    def __str__(self):
        return (f"Asignación {self._id_asignacion} - Empleado ID: {self._empleado_id} - "
                f"Habitación: {self._habitacion_numero} - Fecha: {self._fecha_asignacion} - Tarea: {self._tarea}")

    # Getters y Setters
    @property
    def id_asignacion(self):
        return self._id_asignacion

    @id_asignacion.setter
    def id_asignacion(self, id_asignacion):
        self._id_asignacion = id_asignacion

    @property
    def empleado_id(self):
        return self._empleado_id

    @empleado_id.setter
    def empleado_id(self, empleado_id):
        self._empleado_id = empleado_id

    @property
    def habitacion_numero(self):
        return self._habitacion_numero

    @habitacion_numero.setter
    def habitacion_numero(self, habitacion_numero):
        self._habitacion_numero = habitacion_numero

    @property
    def fecha_asignacion(self):
        return self._fecha_asignacion

    @fecha_asignacion.setter
    def fecha_asignacion(self, fecha_asignacion):
        self._fecha_asignacion = fecha_asignacion

    @property
    def tarea(self):
        return self._tarea

    @tarea.setter
    def tarea(self, tarea):
        self._tarea = tarea
