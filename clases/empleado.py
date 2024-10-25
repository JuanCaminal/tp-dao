class Empleado:
    def init(self, id_empleado, nombre, apellido, cargo, sueldo):
        self._id_empleado = id_empleado
        self._nombre = nombre
        self._apellido = apellido
        self._cargo = cargo
        self._sueldo = sueldo

    def str(self):
        return f"Empleado {self._nombre} {self._apellido} - Cargo: {self._cargo} - Sueldo: {self._sueldo}"

    # Getters y Setters
    @property
    def id_empleado(self):
        return self._id_empleado

    @id_empleado.setter
    def id_empleado(self, id_empleado):
        self._id_empleado = id_empleado

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def apellido(self):
        return self._apellido
    
    @apellido.setter
    def apellido(self, apellido):
        self._apellido = apellido

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, cargo):
        self._cargo = cargo

    @property
    def sueldo(self):
        return self._sueldo

    @sueldo.setter
    def sueldo(self, sueldo):
        self._sueldo = sueldo