import datetime

class Reserva:
    def __init__(self, cliente, habitacion, fecha_entrada, fecha_salida, cantidad_personas, id_reserva=None):
        self._id_reserva = id_reserva
        self._cliente = cliente
        self._habitacion = habitacion
        self._fecha_entrada = fecha_entrada
        self._fecha_salida = fecha_salida
        self._cantidad_personas = cantidad_personas

    

    def __str__(self):
        return f'Reserva {self.id_reserva} - Cliente: {self.cliente.nombre} {self.cliente.apellido} - Habitación: {self.habitacion.numero} - Fechas: {self.fecha_entrada} a {self.fecha_salida}'
    
    # def duracion_estancia(self):
    #     return (self._fecha_salida - self._fecha_entrada).days

    # Getters y Setters
    @property
    def id_reserva(self):
        return self._id_reserva

    @id_reserva.setter
    def id_reserva(self, id_reserva):
        self._id_reserva = id_reserva
        
    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, cliente):
        self._cliente = cliente

    @property
    def habitacion(self):
        return self._habitacion

    @habitacion.setter
    def habitacion(self, habitacion):
        self._habitacion = habitacion
        
        
    @property
    def fecha_entrada(self):
        return self._fecha_entrada

    @fecha_entrada.setter
    def fecha_entrada(self, fecha_entrada):
        self._fecha_entrada = fecha_entrada

    @property
    def fecha_salida(self):
        return self._fecha_salida

    @fecha_salida.setter
    def fecha_salida(self, fecha_salida):
        self._fecha_salida = fecha_salida
        
    @property
    def cantidad_personas(self):
        return self._cantidad_personas

    @cantidad_personas.setter
    def cantidad_personas(self, cantidad_personas):
        self._cantidad_personas = cantidad_personas