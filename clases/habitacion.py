class Habitacion:
    # dunder init method -> instance method
    def __init__(self, numero, tipo, estado, precio_por_noche):    # inicializacion de objetos en Python
        self._numero = numero
        self.tipo = tipo  # Puede ser 'simple', 'doble', o 'suite'
        self._estado = estado  # 'disponible' o 'ocupada'
        self._precio_por_noche = precio_por_noche
    
    # dunder str method    
    def __str__(self):  # se ejecuta cuando se trata de convertir al objeto en string
        # return f"{self.numero} from {self.house}"
        ...
    
    # Getters y Setters
    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado
    
    @property
    def precio_por_noche(self):
        return self._precio_por_noche

    @precio_por_noche.setter
    def precio_por_noche(self, precio):
        self._precio_por_noche = precio
    
    # ir a bd y registrar habitacion
    def registrar_habitacion(self):
        ...
        