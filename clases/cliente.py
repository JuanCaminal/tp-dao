class Cliente:
    def __init__(self, nombre, apellido, direccion, telefono, email, nro_documento, id_cliente=None, puntos_fidelizacion=0, puntos_fidelizacion_canjeados=0):
        self._id_cliente = id_cliente
        self._nombre = nombre
        self._apellido = apellido
        self._direccion = direccion
        self._telefono = telefono
        self._email = email
        self._nro_documento = nro_documento
        self._puntos_fidelizacion = puntos_fidelizacion
        self._puntos_fidelizacion_canjeados = puntos_fidelizacion_canjeados

    def str(self):
        return f'Cliente {self.nombre} {self.apellido} - ID: {self.id_cliente}'

    # Getters y Setters
    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, id_cliente):
        self._id_cliente = id_cliente

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
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, direccion):
        self._direccion = direccion

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        self._telefono = telefono

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def nro_documento(self):
        return self._nro_documento

    @nro_documento.setter
    def nro_documento(self, nro_documento):
        self._nro_documento = nro_documento

    @property
    def puntos_fidelizacion(self):
        return self._puntos_fidelizacion

    @puntos_fidelizacion.setter
    def puntos_fidelizacion(self, puntos):
        self._puntos_fidelizacion = puntos

    @property
    def puntos_fidelizacion_canjeados(self):
        return self._puntos_fidelizacion_canjeados

    @puntos_fidelizacion.setter
    def puntos_fidelizacion_canjeados(self, puntos):
        self._puntos_fidelizacion_canjeados = puntos
