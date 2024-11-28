import datetime

class Factura:
    def __init__(self, id_factura, cliente, reserva, fecha_emision, total):
        self._id_factura = id_factura
        self._cliente = cliente
        self._reserva = reserva
        self._fecha_emision = fecha_emision
        self._total = total

    def calcular_total(self):
        noches = self._reserva.duracion_estancia()
        return noches * self._reserva.habitacion.precio_por_noche

    def str(self):
        return f"Factura {self._id_factura} - Cliente: {self._cliente.nombre} {self._cliente.apellido} - Total: {self._total} - Fecha de emisión: {self._fecha_emision}"

    # Getters y Setters
    @property
    def id_factura(self):
        return self._id_factura

    @id_factura.setter
    def id_factura(self, id_factura):
        self._id_factura = id_factura

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, cliente):
        self._cliente = cliente

    @property
    def reserva(self):
        return self._reserva
    @reserva.setter
    def reserva(self, reserva):
        self._reserva = reserva

    @property
    def fecha_emision(self):
        return self._fecha_emision

    @fecha_emision.setter
    def fecha_emision(self, fecha_emision):
        self._fecha_emision = fecha_emision

    @property
    def total(self):
        return self._total